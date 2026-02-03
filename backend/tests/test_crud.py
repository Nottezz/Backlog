import pytest
from api import crud
from models import Movie
from schemas.movie import MovieCreate, MovieRead
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_create_movie(session: AsyncSession, superuser):
    movie_in = MovieCreate(
        title="Movie Title",
    )
    movie: MovieRead = await crud.create_movie(session, movie_in, superuser)

    assert movie.title == movie_in.title
    assert movie.user == superuser.email.split("@")[0]

    movie_in_db = await session.get(Movie, movie_in.id)
    assert movie_in_db is not None
    assert movie_in_db.title == movie_in.title
