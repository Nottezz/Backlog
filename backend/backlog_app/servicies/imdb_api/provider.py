import logging
from http import HTTPMethod
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class IMDBProviderError(Exception):
    """Base IMDB provider exception."""


class TitleNotFoundError(IMDBProviderError):
    """Movie or TV show was not found."""


class IMDBProvider:
    def __init__(
        self,
        base_url: str,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.client = client or httpx.AsyncClient()

    async def _request(
        self,
        method: HTTPMethod,
        endpoint: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | list[Any] | None = None,
    ) -> dict[str, Any]:
        try:
            response = await self.client.request(
                method=method,
                url=f"{self.base_url}/{endpoint}",
                params=params,
                json=data,
            )

            response.raise_for_status()

            return response.json()

        except httpx.HTTPStatusError as e:
            logger.exception(
                "IMDB API returned HTTP %s",
                e.response.status_code,
            )
            raise IMDBProviderError(
                f"IMDB API returned {e.response.status_code}"
            ) from e

        except httpx.HTTPError as e:
            logger.exception("IMDB API request failed")
            raise IMDBProviderError("IMDB API request failed") from e

    async def search_title(
        self,
        title: str,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        response = await self._request(
            HTTPMethod.GET,
            endpoint="search/titles",
            params={
                "query": title,
                "limit": limit,
            },
        )

        return response.get("titles", [])

    async def get_title_id(
        self,
        title: str,
        year: int | None = None,
    ) -> str:
        titles = await self.search_title(title)

        if not titles:
            raise TitleNotFoundError(f"Title '{title}' not found")

        if year is not None:
            for item in titles:
                if item.get("startYear") == year:
                    logger.debug(
                        "Found title '%s' by year %s",
                        title,
                        year,
                    )
                    return item["id"]

        def popularity_score(item: dict[str, Any]) -> float:
            rating = item.get("rating", {}).get("aggregateRating", 0)

            votes = item.get("rating", {}).get("voteCount", 0)

            return rating * votes

        best_match = max(
            titles,
            key=popularity_score,
        )

        logger.warning(
            "No exact year match for '%s' (%s), " "using most popular result '%s'",
            title,
            year,
            best_match.get("primaryTitle"),
        )

        return best_match["id"]

    async def get_title(
        self,
        title: str,
        year: int | None = None,
    ) -> dict[str, Any]:
        title_id = await self.get_title_id(
            title=title,
            year=year,
        )

        logger.debug(
            "Fetching imdb title %s for '%s'",
            title_id,
            title,
        )

        return await self._request(
            HTTPMethod.GET,
            endpoint=f"titles/{title_id}",
        )
