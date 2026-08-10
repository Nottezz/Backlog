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
    imdb = IMDBProvider(api_key=settings.omdb.api_key)
    title_id = await imdb.get_title_id(title, year)

    assert title_id is not None
    assert "tt" in title_id


@pytest.mark.asyncio
async def test_get_title_success(monkeypatch):
    imdb = IMDBProvider(api_key="test-key")

    mock_get_id = AsyncMock(return_value="tt0816692")
    mock_request = AsyncMock(return_value={"imdbID": "tt0816692", "Response": "True"})

    monkeypatch.setattr(imdb, "get_title_id", mock_get_id)
    monkeypatch.setattr(imdb, "_request", mock_request)

    result = await imdb.get_title("Interstellar", 2014)

    mock_get_id.assert_awaited_once_with(title="Interstellar", year=2014)
    mock_request.assert_awaited_once_with({"i": "tt0816692", "plot": "full"})

    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_get_title_with_rating_and_metacritic(monkeypatch):
    imdb = IMDBProvider(api_key="test-key")

    mock_title_data = {
        "imdbRating": "8.6",
        "Metascore": "74",
        "Response": "True",
    }

    monkeypatch.setattr(imdb, "get_title_id", AsyncMock(return_value="tt0816692"))
    monkeypatch.setattr(imdb, "_request", AsyncMock(return_value=mock_title_data))

    result = await imdb.get_title("Interstellar", 2014)

    assert result["rating"]["aggregateRating"] == 8.6
    assert result["metacritic"]["score"] == 74


@pytest.mark.asyncio
async def test_get_title_without_metacritic(monkeypatch):
    imdb = IMDBProvider(api_key="test-key")

    mock_title_data = {
        "imdbRating": "7.1",
        "Metascore": "N/A",
        "Response": "True",
    }

    monkeypatch.setattr(imdb, "get_title_id", AsyncMock(return_value="tt0317219"))
    monkeypatch.setattr(imdb, "_request", AsyncMock(return_value=mock_title_data))

    result = await imdb.get_title("Cars", 2006)

    assert result["rating"]["aggregateRating"] == 7.1
    assert result.get("metacritic") is None


@pytest.mark.asyncio
async def test_get_title_empty_data(monkeypatch):
    imdb = IMDBProvider(api_key="test-key")

    monkeypatch.setattr(imdb, "get_title_id", AsyncMock(return_value="tt0000000"))
    monkeypatch.setattr(imdb, "_request", AsyncMock(return_value={"Response": "True"}))

    result = await imdb.get_title("Unknown", 0)

    assert result.get("rating") is None
    assert result.get("metacritic") is None
