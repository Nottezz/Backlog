from fastapi import HTTPException
from models import User
from models.movie import Movie
from schemas.movie import MovieCreate, MovieRead, MovieUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


async def create_movie(
    db: AsyncSession, movie_in: MovieCreate, user: User
) -> MovieRead:
    movie = Movie(**movie_in.model_dump(), user_id=user.id)
    db.add(movie)
    await db.commit()
    await db.refresh(movie)

    return MovieRead(
        id=movie.id,
        title=movie.title,
        description=movie.description,
        year=movie.year,
        rating=movie.rating,
        kp_id=movie.kp_id,
        imdb_id=movie.imdb_id,
        watch_link=movie.watch_link,
        watched=movie.watched,
        created_at=movie.created_at,
        user=user.email.split("@")[0],
    )


async def get_movies(db: AsyncSession, user_id: str | None = None):
    query = select(Movie).options(selectinload(Movie.user))

    if user_id is not None:
        query = query.where(Movie.user_id == user_id)

    result = await db.execute(query)
    movies = result.scalars().all()
    return [
        MovieRead(
            id=m.id,
            title=m.title,
            description=m.description,
            year=m.year,
            rating=m.rating,
            imdb_id=m.imdb_id,
            watch_link=m.watch_link,
            watched=m.watched,
            created_at=m.created_at,
            kp_id=m.kp_id,
            user=m.user.email.split("@")[0],
        )
        for m in movies
    ]


async def get_movie_by_id(
    db: AsyncSession, movie_id: int, user_id: int | None = None
) -> MovieRead | None:
    query = select(Movie).options(selectinload(Movie.user)).where(Movie.id == movie_id)

    if user_id is not None:
        query = query.where(Movie.user_id == user_id)

    result = await db.execute(query)
    movie = result.scalars().first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    return MovieRead(
        id=movie.id,
        title=movie.title,
        description=movie.description,
        year=movie.year,
        rating=movie.rating,
        imdb_id=movie.imdb_id,
        watch_link=movie.watch_link,
        watched=movie.watched,
        created_at=movie.created_at,
        kp_id=movie.kp_id,
        user=movie.user.email.split("@")[0],
    )


async def update_movie(
    db: AsyncSession,
    movie_id: int,
    movie_in: MovieUpdate,
    user: User,
) -> MovieRead:
    result = await db.execute(
        select(Movie).options(selectinload(Movie.user)).where(Movie.id == movie_id)
    )
    movie = result.scalars().first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    check_movie_ownership(movie, user)

    for field, value in movie_in.model_dump(exclude_unset=True).items():
        setattr(movie, field, value)

    await db.commit()
    await db.refresh(movie)

    return MovieRead(
        id=movie.id,
        title=movie.title,
        description=movie.description,
        year=movie.year,
        rating=movie.rating,
        kp_id=movie.kp_id,
        imdb_id=movie.imdb_id,
        watch_link=movie.watch_link,
        watched=movie.watched,
        user=movie.user.email.split("@")[0],
        created_at=movie.created_at.isoformat(),
    )


async def partial_update_movie(
    db: AsyncSession, movie_id: int, movie_in: MovieUpdate
) -> Movie | None:
    result = await db.execute(select(Movie).where(Movie.id == movie_id))
    movie = result.scalars().first()
    if not movie:
        raise HTTPException(status_code=404)

    for field, value in movie_in.model_dump(exclude_unset=True).items():
        setattr(movie, field, value)

    await db.commit()
    await db.refresh(movie)
    return movie


async def delete_movie(
    db: AsyncSession,
    movie_id: int,
    user: User,
) -> Movie | None:
    result = await db.execute(select(Movie).where(Movie.id == movie_id))
    movie = result.scalars().first()
    if not movie:
        raise HTTPException(status_code=404)

    check_movie_ownership(movie, user)

    await db.delete(movie)
    await db.commit()
    return movie


def check_movie_ownership(movie: Movie, user: User) -> None:
    """Проверяет, может ли пользователь изменять фильм"""
    if not user.is_superuser and movie.user_id != user.id:
        raise HTTPException(
            status_code=403, detail="You don't have access to this action"
        )
