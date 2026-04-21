from typing import Generator

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool
from starlette.testclient import TestClient

from backlog_app.config import settings
from backlog_app.main import app
from backlog_app.storages.database import get_async_session

TEST_USERNAME = "test_user@example.com"
TEST_PASSWORD = "testuser"


@pytest.fixture(scope="function")
def client():
    test_engine = create_async_engine(
        settings.db.connection.database_url_asyncpg,
        poolclass=NullPool,
    )
    test_session_factory = async_sessionmaker(
        test_engine,
        expire_on_commit=False,
    )

    async def override_get_async_session():
        async with test_session_factory() as session:
            yield session

    app.dependency_overrides[get_async_session] = override_get_async_session

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def access_token(client) -> str:
    response = client.post(
        "/api/auth/login",
        data={
            "username": TEST_USERNAME,
            "password": TEST_PASSWORD,
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def auth_client(access_token: str) -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        client.headers.update({"Authorization": f"Bearer {access_token}"})
        yield client
