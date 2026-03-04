from http import HTTPMethod
from unittest.mock import AsyncMock

import pytest

from backlog_app.config import settings
from backlog_app.servicies.imdb_api.provider import IMDBProvider


@pytest.mark.parametrize(
    "title, year",
    [
        pytest.param("Interstellar", 2014),
        pytest.param("The Fast and the Furious", None),
    ],
)
@pytest.mark.asyncio
async def test_get_title_id(title, year):
    imdb = IMDBProvider(base_url=settings.imdb_url)
    title_id = await imdb.get_title_id(title, year)

    assert title_id is not None
    assert "tt" in title_id


@pytest.mark.asyncio
async def test_get_title_success(monkeypatch):
    imdb = IMDBProvider(base_url="https://mocked-api.com")

    mock_get_id = AsyncMock(return_value="tt0816692")
    mock_request = AsyncMock(return_value={"id": "tt0816692"})

    monkeypatch.setattr(imdb, "get_title_id", mock_get_id)
    monkeypatch.setattr(imdb, "_request", mock_request)

    result = await imdb.get_title("Interstellar")

    mock_get_id.assert_awaited_once_with("Interstellar")
    mock_request.assert_awaited_once_with(
        HTTPMethod.GET,
        endpoint="titles/tt0816692",
    )

    assert result == {"id": "tt0816692"}


@pytest.mark.asyncio
async def test_get_title_rating_success(monkeypatch):
    imdb = IMDBProvider(base_url="https://mocked-api.com")

    mock_title_data = {
        "rating": {"aggregateRating": 8.6},
        "metacritic": {"score": 74},
    }

    mock_get_title = AsyncMock(return_value=mock_title_data)
    monkeypatch.setattr(imdb, "get_title", mock_get_title)

    imdb_rating, metacritic_score = await imdb.get_title_rating("Interstellar")

    mock_get_title.assert_awaited_once_with("Interstellar")
    assert imdb_rating == 8.6
    assert metacritic_score == 74


@pytest.mark.asyncio
async def test_get_title_rating_without_metacritic(monkeypatch):
    imdb = IMDBProvider(base_url="https://mocked-api.com")

    mock_title_data = {"rating": {"aggregateRating": 7.1}}

    monkeypatch.setattr(
        imdb,
        "get_title",
        AsyncMock(return_value=mock_title_data),
    )

    imdb_rating, metacritic_score = await imdb.get_title_rating("Cars")

    assert imdb_rating == 7.1
    assert metacritic_score is None


@pytest.mark.asyncio
async def test_get_title_rating_empty_data(monkeypatch):
    imdb = IMDBProvider(base_url="https://mocked-api.com")

    monkeypatch.setattr(
        imdb,
        "get_title",
        AsyncMock(return_value={}),
    )

    imdb_rating, metacritic_score = await imdb.get_title_rating("Unknown")

    assert imdb_rating is None
    assert metacritic_score is None
