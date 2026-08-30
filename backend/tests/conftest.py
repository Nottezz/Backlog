import contextlib
import os
from typing import AsyncGenerator

import pytest
from sqlalchemy import event
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.future import select

from backlog_app._helpers.create_super_user import create_user
from backlog_app.api.crud import create_movie, delete_movie
from backlog_app.dependencies.authentification.user_manager import get_user_manager
from backlog_app.dependencies.authentification.users import get_user_db
from backlog_app.models import Base, Movie, User
from backlog_app.schemas.movie import MovieCreate, MovieRead
from backlog_app.schemas.user import UserCreate

DB_PATH = "test.db"
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

engine_test = create_async_engine(DATABASE_URL, echo=False)


@event.listens_for(engine_test.sync_engine, "connect")
def _set_sqlite_foreign_keys(dbapi_connection, _connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


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

    await engine_test.dispose()

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
        password="testpassword",
        is_active=True,
        is_superuser=False,
        is_verified=True,
    )

    async with get_user_db_context() as user_db:
        async with get_user_manager_context(user_db) as user_manager:
            user = await create_user(user_manager=user_manager, user_create=user_create)
            yield user
            await user_manager.delete(user)


def build_movie_create(
    title: str, rating: float, watch_link: str, description: str
) -> MovieCreate:
    return MovieCreate(
        title=title,
        description=description,
        rating=rating,
        imdb_id=123456789,
        watch_link=watch_link,
    )


@pytest.fixture
async def movie(session, user_test) -> AsyncGenerator[MovieRead, None]:
    movie_in = build_movie_create(
        "Interstellar", 9.5, "https://example.com", "Interstellar" * 20
    )
    movie = await create_movie(session, movie_in, user_test)
    yield movie
    try:
        await delete_movie(session, movie.slug, user_test)
    except Exception:
        pass


async def _make_user(session, email: str) -> AsyncGenerator[User, None]:
    get_user_db_context = contextlib.asynccontextmanager(lambda: get_user_db(session))
    get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)
    user_create = UserCreate(
        email=email,
        password="testpassword",
        is_active=True,
        is_superuser=False,
        is_verified=True,
    )
    async with get_user_db_context() as user_db:
        async with get_user_manager_context(user_db) as user_manager:
            user = await create_user(user_manager=user_manager, user_create=user_create)
            yield user
            await user_manager.delete(user)


@pytest.fixture
async def user_other(session) -> AsyncGenerator[User, None]:
    async for user in _make_user(session, "other_user@test.com"):
        yield user


@pytest.fixture
async def published_movie(session, user_test) -> AsyncGenerator[Movie, None]:
    movie_in = MovieCreate(
        title="Published Test Movie",
        description="A movie for testing many-to-many features.",
        published=True,
    )
    movie_read = await create_movie(session, movie_in, user_test)
    result = await session.execute(select(Movie).where(Movie.slug == movie_read.slug))
    movie = result.scalars().first()
    yield movie
    try:
        await delete_movie(session, movie.slug, user_test)
    except Exception:
        pass
