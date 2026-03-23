import asyncio
import logging
from http import HTTPMethod

import httpx
from fastapi import HTTPException

logger = logging.getLogger(__name__)


class IMDBProvider:
    """
    IMDB API provider
    """

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    async def _request(
        self,
        method: HTTPMethod,
        endpoint: str,
        params: dict | None = None,
        data: dict | list | None = None,
    ) -> dict:
        url = f"{self.base_url}/{endpoint}"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                status_code = getattr(e.response, "status_code", 500)
                logger.error(
                    "IMDB API error. Status code: %s, detail: %s", status_code, e
                )
                raise HTTPException(
                    status_code=status_code, detail="SERVER_ERROR"
                ) from e

    async def get_title_id(self, title: str, year: int) -> str:
        """
        title identifier is of type str, because the imdb identifier is tt0816692
        """
        params = {"query": title, "limit": 10}
        response = await self._request(
            HTTPMethod.GET,
            endpoint="search/titles",
            params=params,
        )
        titles = response.get("titles")
        if not titles:
            raise HTTPException(status_code=404, detail="Title not found")

        logger.debug("TITLE YEAR: %s", year)
        if year:
            for t in titles:
                if t.get("startYear") == year:
                    logger.debug("Found match by year: %s", t)
                    return t["id"]

        def popularity_score(t):
            rating = t.get("rating", {}).get("aggregateRating", 0)
            votes = t.get("rating", {}).get("voteCount", 0)
            return rating * votes

        best_match = max(titles, key=popularity_score)
        logger.warning(
            "No title found for year %s, using most popular match: %s", year, best_match
        )
        return best_match["id"]

    async def get_title(self, title: str, year: int) -> dict:
        title_id = await self.get_title_id(title, year)
        return await self._request(HTTPMethod.GET, endpoint=f"titles/{title_id}")

    async def get_title_rating(self, title: str, year: int) -> tuple[float, float]:
        title_data = await self.get_title(title, year)

        rating = title_data.get("rating", {})
        metacritic_rating = title_data.get("metacritic", {})

        logger.debug("Found title info: %s", title_data)
        logger.debug("Title Rating: %s, %s", rating, metacritic_rating)

        return rating.get("aggregateRating"), metacritic_rating.get("score")

    async def get_title_description(self, title: str, year: int) -> str:
        title_data = await self.get_title(title, year)

        description = title_data.get("plot")

        logger.debug("Found title info: %s", title_data)
        logger.debug("Title Description: %s", description)

        return description
