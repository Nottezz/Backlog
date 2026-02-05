from typing import Generator

import pytest
from starlette.testclient import TestClient

from backlog_app.main import app

TEST_USERNAME = "test_user@example.com"
TEST_PASSWORD = "testuser"

@pytest.fixture
def client():
    return TestClient(app)


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
