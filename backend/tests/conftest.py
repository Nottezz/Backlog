import pytest
from typing import Generator
from fastapi.testclient import TestClient

from backend.backlog_app.main import app

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
import os
from models import Base, User, Movie, AccessToken
from _helpers.create_super_user import create_super_user

DB_PATH = "test.db"
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

engine_test = create_async_engine(DATABASE_URL, echo=True) # todo: change to False
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
def client() -> Generator[TestClient]:
    with TestClient(app) as client:
        yield client
