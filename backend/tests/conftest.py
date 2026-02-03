import pytest
from typing import Generator
from fastapi.testclient import TestClient

from backend.backlog_app.main import app

@pytest.fixture
def client() -> Generator[TestClient]:
    with TestClient(app) as client:
        yield client
