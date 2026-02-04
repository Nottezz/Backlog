from uuid import uuid4

import pytest
from fastapi import HTTPException, status

from api import crud
from models import Movie, User
from schemas.movie import MovieCreate, MovieRead, MovieUpdate
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_create_movie(
    session: AsyncSession,
    user_test: User,
) -> None:
    movie_in = MovieCreate(
        title="Movie Title",
        rating=8.5,
        watch_link="https://example.com",
        description="Movie Description",
        imdb_id=1234,
    )
    movie: MovieRead = await crud.create_movie(session, movie_in, user_test)

    assert movie.title == movie_in.title
    assert movie.description == movie_in.description
    assert movie.imdb_id == movie_in.imdb_id
    assert movie.watch_link == movie_in.watch_link
    assert movie.rating == movie_in.rating
    assert movie.user == user_test.email.split("@")[0]

    movie_in_db = await session.get(Movie, movie.id)
    assert movie_in_db is not None
    assert movie_in_db.title == movie_in.title
    assert movie_in_db.description == movie_in.description
    assert movie_in_db.imdb_id == movie_in.imdb_id
    assert movie_in_db.watch_link == movie_in.watch_link
    assert movie_in_db.rating == movie_in.rating

@pytest.mark.asyncio
async def test_get_movie_by_id(
    session: AsyncSession,
    user_test: User,
    movie: Movie,
) -> None:
    result = await crud.get_movie_by_id(
        db=session,
        movie_id=movie.id,
        user_id=user_test.id,
    )

    assert result.id == movie.id
    assert result.title == movie.title
    assert result.rating == movie.rating
    assert result.imdb_id == movie.imdb_id
    assert result.watch_link == movie.watch_link

    assert result.user == user_test.email.split("@")[0]

@pytest.mark.asyncio
async def test_get_movie_by_id_wrong_user(
    session: AsyncSession,
    movie: Movie,
):
    wrong_user_id = uuid4()

    with pytest.raises(HTTPException) as exc:
        await crud.get_movie_by_id(
            db=session,
            movie_id=movie.id,
            user_id=wrong_user_id,
        )

    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc.value.detail == "Movie not found"

@pytest.mark.asyncio
async def test_update_movie(
        session: AsyncSession,
        user_test: User,
        movie: Movie,
):
    movie_in = MovieUpdate(
        title="Movie Title x2",
        rating=5.5,
        watch_link="https://example.com/example",
    )

    movie = await crud.update_movie(
        db=session,
        movie_id=movie.id,
        user=user_test,
        movie_in=movie_in
    )

    assert movie.title == movie_in.title
    assert movie.description == movie_in.description
    assert movie.imdb_id == movie_in.imdb_id
    assert movie.watch_link == movie_in.watch_link
    assert movie.rating == movie_in.rating
    assert movie.user == user_test.email.split("@")[0]

    movie_in_db = await session.get(Movie, movie.id)
    assert movie_in_db is not None
    assert movie_in_db.title == movie_in.title
    assert movie_in_db.description == movie_in.description
    assert movie_in_db.imdb_id == movie_in.imdb_id
    assert movie_in_db.watch_link == movie_in.watch_link
    assert movie_in_db.rating == movie_in.rating

async def test_delete_movie(session: AsyncSession, user_test: User):
    movie_in = MovieCreate(
        title="Movie Title",
        rating=8.5,
        watch_link="https://example.com",
        description="Movie Description",
        imdb_id=1234,
    )
    movie: MovieRead = await crud.create_movie(session, movie_in, user_test)
    assert movie.title == movie_in.title

    await crud.delete_movie(session, movie.id, user_test)
    movie_in_db = await session.get(Movie, movie.id)
    assert movie_in_db is None
