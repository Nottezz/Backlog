import logging
from typing import Any

import httpx
from config import settings

logger = logging.getLogger(__name__)


class IMDBProviderError(Exception):
    """Base IMDB provider exception."""


class TitleNotFoundError(IMDBProviderError):
    """Movie or TV show was not found."""


class IMDBProvider:
    def __init__(
        self,
        api_key: str,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.api_key = api_key
        self.client = client or httpx.AsyncClient()

    async def _request(self, params: dict[str, Any]) -> dict[str, Any]:
        try:
            response = await self.client.get(
                settings.omdb.base_url,
                params={"apikey": self.api_key, **params},
            )
            response.raise_for_status()
            data = response.json()

            if data.get("Response") == "False":
                raise TitleNotFoundError(data.get("Error", "Not found"))

            return data

        except TitleNotFoundError:
            raise

        except httpx.HTTPStatusError as e:
            logger.exception("OMDb API returned HTTP %s", e.response.status_code)
            raise IMDBProviderError(
                f"OMDb API returned {e.response.status_code}"
            ) from e

        except httpx.HTTPError as e:
            logger.exception("OMDb API request failed")
            raise IMDBProviderError("OMDb API request failed") from e

    async def search_title(
        self,
        title: str,
        year: int | None = None,
    ) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"s": title}
        if year is not None:
            params["y"] = year
        response = await self._request(params)
        return response.get("Search", [])

    async def get_title_id(
        self,
        title: str,
        year: int | None = None,
    ) -> str:
        results = await self.search_title(title, year)

        if not results and year is not None:
            logger.warning(
                "No results for '%s' (%s), retrying without year filter",
                title,
                year,
            )
            results = await self.search_title(title)

        if not results:
            raise TitleNotFoundError(f"Title '{title}' not found")

        return results[0]["imdbID"]

    async def get_title(
        self,
        title: str,
        year: int | None = None,
    ) -> dict[str, Any]:
        title_id = await self.get_title_id(title=title, year=year)

        logger.debug("Fetching OMDb title %s for '%s'", title_id, title)

        raw = await self._request({"i": title_id, "plot": "full"})
        return self._normalize(raw)

    def _normalize(self, raw: dict[str, Any]) -> dict[str, Any]:
        result: dict[str, Any] = {}

        imdb_rating = raw.get("imdbRating")
        if imdb_rating and imdb_rating != "N/A":
            result["rating"] = {"aggregateRating": float(imdb_rating)}

        metascore = raw.get("Metascore")
        if metascore and metascore != "N/A":
            result["metacritic"] = {"score": int(metascore)}

        plot = raw.get("Plot")
        if plot and plot != "N/A":
            result["plot"] = plot

        return result
