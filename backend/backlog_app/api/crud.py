import logging
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload

from backlog_app._helpers.slug_helper import generate_unique_slug
from backlog_app.models import User
from backlog_app.models.movie import Movie
from backlog_app.models.user_movie import UserMovie
from backlog_app.schemas.movie import MovieCreate, MovieList, MovieRead, MovieUpdate
from backlog_app.schemas.user import UserRead

logger = logging.getLogger(__name__)


def build_movie_read(
    movie: Movie,
    user_movie: UserMovie | None,
    joined_by: list[UserRead] | None = None,
) -> MovieRead:
    watched = user_movie.watched if user_movie else False
    note = user_movie.note if user_movie else None
    rating = user_movie.rating if user_movie else None
    is_joined = user_movie is not None and user_movie.user_id != movie.user_id
    return MovieRead.model_validate(
        {
            **{c.name: getattr(movie, c.name) for c in movie.__table__.columns},
            "user": movie.user,
            "watched": watched,
            "note": note,
            "rating": rating,
            "is_joined": is_joined,
            "joined_by": joined_by or [],
        }
    )


async def create_user_movie(
    db: AsyncSession,
    user_id: UUID,
    movie_id: int,
    watched: bool = False,
    note: str | None = None,
    rating: float | None = None,
) -> UserMovie:
    result = await db.execute(
        select(UserMovie).where(
            UserMovie.user_id == user_id,
            UserMovie.movie_id == movie_id,
        )
    )
    existing = result.scalars().first()
    if existing:
        return existing

    user_movie = UserMovie(
        user_id=user_id,
        movie_id=movie_id,
        watched=watched,
        note=note,
        rating=rating,
    )
    db.add(user_movie)
    await db.flush()
    return user_movie


async def delete_user_movie(
    db: AsyncSession,
    user_id: UUID,
    movie_id: int,
) -> None:
    result = await db.execute(
        select(UserMovie).where(
            UserMovie.user_id == user_id,
            UserMovie.movie_id == movie_id,
        )
    )
    user_movie = result.scalars().first()
    if not user_movie:
        raise HTTPException(status_code=404, detail="Not joined to this movie")

    await db.delete(user_movie)
    await db.flush()


async def create_movie(
    db: AsyncSession, movie_in: MovieCreate, user: User
) -> MovieRead:
    movie_fields = movie_in.model_dump(exclude={"watched", "note", "rating"})
    slug = await generate_unique_slug(db=db, title=movie_in.title)
    movie = Movie(**movie_fields, slug=slug, user_id=user.id)
    db.add(movie)
    await db.flush()  # get movie.id before creating UserMovie

    user_movie = await create_user_movie(
        db,
        user.id,
        movie.id,
        watched=movie_in.watched or False,
        note=movie_in.note,
        rating=movie_in.rating,
    )
    await db.commit()
    await db.refresh(movie)
    await db.refresh(user_movie)
    movie.user = user  # relationship not loaded by refresh; set explicitly

    logger.info("Movie <%s> has been created.", movie.slug)

    return build_movie_read(movie, user_movie)


async def get_movies(
    db: AsyncSession,
    filter_user_id: UUID | None = None,
    current_user_id: UUID | None = None,
) -> MovieList:
    query = select(Movie).options(joinedload(Movie.user))

    if filter_user_id is not None:
        query = query.where(Movie.user_id == filter_user_id)
    else:
        query = query.where(
            or_(Movie.published.is_(True), Movie.user_id == current_user_id)
        )

    result = await db.execute(query)
    movies = result.scalars().all()

    logger.debug("Size of movies list: %s", len(movies))

    # Batch-load UserMovies for current user to avoid N+1
    user_movie_map: dict[int, UserMovie] = {}
    if current_user_id is not None and movies:
        um_result = await db.execute(
            select(UserMovie).where(
                UserMovie.user_id == current_user_id,
                UserMovie.movie_id.in_([m.id for m in movies]),
            )
        )
        user_movie_map = {um.movie_id: um for um in um_result.scalars().all()}

    movie_reads = [
        build_movie_read(movie, user_movie_map.get(movie.id), joined_by=[])
        for movie in movies
    ]

    return MovieList.model_validate({"movies": movie_reads})


async def get_random_movie_pool(
    db: AsyncSession,
    user_id: UUID,
    exclude_ids: list[int] | None = None,
) -> list[Movie]:
    if exclude_ids is None:
        exclude_ids = []

    # Return published or owned movies where the user hasn't watched them yet
    query = (
        select(Movie)
        .where(
            or_(Movie.published.is_(True), Movie.user_id == user_id),
        )
        .join(
            UserMovie,
            (UserMovie.movie_id == Movie.id) & (UserMovie.user_id == user_id),
            isouter=True,
        )
        .where(or_(UserMovie.watched.is_(False), UserMovie.watched.is_(None)))
    )

    if exclude_ids:
        query = query.where(Movie.id.notin_(exclude_ids))

    result = await db.execute(query)
    pool = result.scalars().all()

    logger.debug(
        "Random movie pool size: %s (excluded: %s)", len(pool), len(exclude_ids)
    )

    return list(pool)


async def get_movie_by_slug(
    db: AsyncSession,
    slug: str,
    current_user_id: UUID,
) -> MovieRead:
    query = (
        select(Movie)
        .options(
            joinedload(Movie.user),
            selectinload(Movie.joined_by_users).selectinload(UserMovie.user),
        )
        .where(Movie.slug == slug)
        .execution_options(populate_existing=True)
    )

    result = await db.execute(query)
    movie = result.scalars().unique().first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    logger.info("Movie has been found.")

    # Find current user's UserMovie for personal state
    um_result = await db.execute(
        select(UserMovie).where(
            UserMovie.user_id == current_user_id,
            UserMovie.movie_id == movie.id,
        )
    )
    user_movie: UserMovie | None = um_result.scalars().first()

    # Build joined_by: all users who joined, excluding the owner
    joined_by: list[UserRead] = [
        UserRead.model_validate(um.user)
        for um in movie.joined_by_users
        if um.user_id != movie.user_id and um.user is not None
    ]

    return build_movie_read(movie, user_movie, joined_by=joined_by)


async def update_movie(
    db: AsyncSession,
    slug: str,
    movie_in: MovieUpdate,
    user: User,
) -> MovieRead:
    result = await db.execute(
        select(Movie)
        .options(
            selectinload(Movie.joined_by_users).selectinload(UserMovie.user),
        )
        .where(Movie.slug == slug)
    )
    movie = result.scalars().first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    check_movie_ownership(movie, user)

    # PUT is owner-only: split fields
    movie_fields = {
        k: v
        for k, v in movie_in.model_dump(exclude_unset=True).items()
        if k not in {"watched", "note", "rating"}
    }
    personal_fields = {
        k: v
        for k, v in movie_in.model_dump(exclude_unset=True).items()
        if k in {"watched", "note", "rating"}
    }

    for field, value in movie_fields.items():
        setattr(movie, field, value)

    if personal_fields:
        user_movie = await create_user_movie(db, user.id, movie.id)
        for field, value in personal_fields.items():
            setattr(user_movie, field, value)

    await db.commit()

    logger.info("Movie has been updated.")

    return await get_movie_by_slug(db, slug, user.id)


async def partial_update_movie(
    db: AsyncSession,
    slug: str,
    movie_in: MovieUpdate,
    user: User,
) -> MovieRead:
    result = await db.execute(
        select(Movie)
        .options(
            selectinload(Movie.joined_by_users).selectinload(UserMovie.user),
        )
        .where(Movie.slug == slug)
    )
    movie = result.scalars().first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    is_owner = movie.user_id == user.id or user.is_superuser

    # Non-owners cannot modify protected fields
    protected_fields = {"title", "description", "year"}
    submitted = set(movie_in.model_dump(exclude_unset=True).keys())
    if not is_owner and submitted & protected_fields:
        raise HTTPException(
            status_code=403,
            detail="Only the owner can edit title, description, or year",
        )

    movie_fields = {
        k: v
        for k, v in movie_in.model_dump(exclude_unset=True).items()
        if k not in {"watched", "note", "rating"}
    }
    personal_fields = {
        k: v
        for k, v in movie_in.model_dump(exclude_unset=True).items()
        if k in {"watched", "note", "rating"}
    }

    # Only owner/superuser can update movie-level fields
    if movie_fields and is_owner:
        for field, value in movie_fields.items():
            setattr(movie, field, value)

    # Update personal state — owner always has UserMovie; non-owner must have already joined
    if personal_fields:
        if is_owner:
            user_movie = await create_user_movie(db, user.id, movie.id)
        else:
            um_result = await db.execute(
                select(UserMovie).where(
                    UserMovie.user_id == user.id,
                    UserMovie.movie_id == movie.id,
                )
            )
            user_movie = um_result.scalars().first()
            if not user_movie:
                raise HTTPException(
                    status_code=403,
                    detail="You must join this movie before updating your personal state",
                )
        for field, value in personal_fields.items():
            setattr(user_movie, field, value)

    await db.commit()

    logger.info("Movie has been partially updated.")

    return await get_movie_by_slug(db, slug, user.id)


async def delete_movie(
    db: AsyncSession,
    slug: str,
    user: User,
) -> None:
    result = await db.execute(select(Movie).where(Movie.slug == slug))
    movie = result.scalars().first()
    if not movie:
        raise HTTPException(status_code=404)

    check_movie_ownership(movie, user)

    await db.delete(movie)
    await db.commit()

    logger.info("Movie <%s> has been deleted.", slug)


def check_movie_ownership(movie: Movie, user: User) -> None:
    logger.debug("Checking movie ownership for user %s", user.id)
    if not user.is_superuser and movie.user_id != user.id:
        raise HTTPException(
            status_code=403, detail="You don't have access to this action"
        )
