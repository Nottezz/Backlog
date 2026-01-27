from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.exceptions import HTTPException

from backlog_app.models.movie import Movie
from backlog_app.schemas.movie import MovieCreate, MovieUpdate


async def create_movie(db: AsyncSession, movie_in: MovieCreate) -> Movie:
    movie = Movie(**movie_in.model_dump())
    db.add(movie)
    await db.commit()
    await db.refresh(movie)
    return movie

async def get_movies(db: AsyncSession):
    result = await db.execute(select(Movie))
    return result.scalars().all()

async def get_movie_by_id(db: AsyncSession, movie_id: int) -> Movie:
    result = await db.execute(select(Movie).where(Movie.id == movie_id))
    return result.scalars().first()

async def update_movie(
    db: AsyncSession, movie_id: int, movie_in: MovieUpdate
) -> Movie | None:
    result = await db.execute(select(Movie).where(Movie.id == movie_id))
    movie = result.scalars().first()

    if not movie:
        raise HTTPException(status_code=404)

    for field, value in movie_in:
        setattr(movie, field, value)

    await db.commit()
    await db.refresh(movie)
    return movie

async def partial_update_movie(db: AsyncSession, movie_id: int, movie_in: MovieUpdate) -> Movie | None:
    result = await db.execute(select(Movie).where(Movie.id == movie_id))
    movie = result.scalars().first()
    if not movie:
        raise HTTPException(status_code=404)

    for field, value in movie_in.model_dump(exclude_unset=True).items():
        setattr(movie, field, value)

    await db.commit()
    await db.refresh(movie)
    return movie

async def delete_movie(db: AsyncSession, movie_id: int) -> Movie | None:
    result = await db.execute(select(Movie).where(Movie.id == movie_id))
    movie = result.scalars().first()
    if not movie:
        raise HTTPException(status_code=404)

    await db.delete(movie)
    await db.commit()
    return movie
