from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from starlette.exceptions import HTTPException

from models import User
from models.movie import Movie
from schemas.movie import MovieCreate, MovieUpdate, MovieRead


async def create_movie(db: AsyncSession, movie_in: MovieCreate, user: User) -> MovieRead:
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
        user=user.email.split("@")[0]
    )


async def get_movies(db: AsyncSession):
    result = await db.execute(
        select(Movie).options(selectinload(Movie.user))
    )
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


async def get_movie_by_id(db: AsyncSession, movie_id: int) -> MovieRead | None:
    result = await db.execute(
        select(Movie)
        .options(selectinload(Movie.user))
        .where(Movie.id == movie_id)
    )
    movie = result.scalars().first()
    if not movie:
        return None
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
    db: AsyncSession, movie_id: int, movie_in: MovieUpdate
) -> MovieRead:
    result = await db.execute(
        select(Movie)
        .options(selectinload(Movie.user))
        .where(Movie.id == movie_id)
    )
    movie = result.scalars().first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

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
        created_at=movie.created_at.isoformat()
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


async def delete_movie(db: AsyncSession, movie_id: int) -> Movie | None:
    result = await db.execute(select(Movie).where(Movie.id == movie_id))
    movie = result.scalars().first()
    if not movie:
        raise HTTPException(status_code=404)

    await db.delete(movie)
    await db.commit()
    return movie
