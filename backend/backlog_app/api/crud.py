import logging
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from backlog_app.models import User
from backlog_app.models.movie import Movie
from backlog_app.schemas.movie import MovieCreate, MovieList, MovieRead, MovieUpdate

logger = logging.getLogger(__name__)


async def create_movie(
    db: AsyncSession, movie_in: MovieCreate, user: User
) -> MovieRead:
    movie = Movie(**movie_in.model_dump(), user_id=user.id)
    db.add(movie)
    await db.commit()
    await db.refresh(movie)

    logger.info("Movie <%s> has been created.", movie.id)

    return MovieRead.model_validate(movie)


async def get_movies(db: AsyncSession, user_id: str | None = None) -> MovieList:
    query = select(Movie).options(selectinload(Movie.user))

    if user_id:
        query = query.where(Movie.user_id == user_id)
    else:
        query = query.where(Movie.published.is_(True))

    result = await db.execute(query)
    movies = result.scalars().all()

    logger.debug("Size of movies list: %s", len(movies))

    return MovieList.model_validate({"movies": movies})


async def get_movie_by_id(
    db: AsyncSession, movie_id: int, user_id: UUID | None = None
) -> MovieRead | None:
    query = select(Movie).options(selectinload(Movie.user)).where(Movie.id == movie_id)

    if user_id is not None:
        query = query.where(Movie.user_id == user_id)

    result = await db.execute(query)
    movie = result.scalars().first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    logger.info("Movie has been found.")

    return MovieRead.model_validate(movie)


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

    logger.info("Movie has been updated.")

    return MovieRead.model_validate(movie)


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
) -> MovieRead:
    result = await db.execute(select(Movie).where(Movie.id == movie_id))
    movie = result.scalars().first()
    if not movie:
        raise HTTPException(status_code=404)

    check_movie_ownership(movie, user)

    await db.delete(movie)
    await db.commit()

    logger.info("Movie <%s> has been deleted.", movie_id)

    return MovieRead.model_validate(movie)


def check_movie_ownership(movie: Movie, user: User) -> None:
    """Проверяет, может ли пользователь изменять фильм"""
    logger.debug("Checking movie ownership for user %s", user.id)
    if not user.is_superuser and movie.user_id != user.id:
        raise HTTPException(
            status_code=403, detail="You don't have access to this action"
        )
