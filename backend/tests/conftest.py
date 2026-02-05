import contextlib
import os
from typing import Any, AsyncGenerator, Generator

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from backlog_app._helpers.create_super_user import create_user
from backlog_app.api.crud import create_movie, delete_movie
from backlog_app.dependencies.authentification.user_manager import get_user_manager
from backlog_app.dependencies.authentification.users import get_user_db
from backlog_app.models import Base, Movie, User
from backlog_app.schemas.movie import MovieCreate, MovieRead
from backlog_app.schemas.user import UserCreate

DB_PATH = "test.db"
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

engine_test = create_async_engine(DATABASE_URL, echo=True)  # todo: change to False
AsyncSessionTest = async_sessionmaker(
    engine_test,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
async def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    async with engine_test.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)


@pytest.fixture
async def session(init_db):
    async with AsyncSessionTest() as session:
        yield session


@pytest.fixture
async def user_test(session) -> AsyncGenerator[User, None]:
    get_user_db_context = contextlib.asynccontextmanager(lambda: get_user_db(session))
    get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)

    user_create = UserCreate(
        email="test_user@test.com",
        password="test",
        is_active=True,
        is_superuser=False,
        is_verified=True,
    )

    async with get_user_db_context() as user_db:
        async with get_user_manager_context(user_db) as user_manager:
            user = await create_user(user_manager=user_manager, user_create=user_create)
            yield user
            await user_manager.delete(user)


def build_movie_create(title: str, rating: float, watch_link: str) -> MovieCreate:
    return MovieCreate(
        title=title,
        rating=rating,
        imdb_id=123456789,
        watch_link=watch_link,
    )


@pytest.fixture
async def movie(session, user_test) -> AsyncGenerator[MovieRead, None]:
    title = "Interstellar"
    rating = 9.5
    watch_link = "https://example.com"
    movie_in = build_movie_create(title, rating, watch_link)

    movie = await create_movie(session, movie_in, user_test)
    yield movie
    await delete_movie(session, movie.id, user_test)
