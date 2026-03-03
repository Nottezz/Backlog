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

    def __init__(self, base_url: str):
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
                raise HTTPException(status_code=status_code, detail=e) from e

    async def get_title_id(self, title: str) -> str:
        """
        title identifier is of type str, because the imdb identifier is tt0816692
        """
        params = {"query": title, "limit": 2}
        response = await self._request(
            HTTPMethod.GET,
            endpoint="search/titles",
            params=params,
        )
        titles = response.get("titles")
        if not titles:
            raise HTTPException(status_code=404, detail="Title not found")
        title_id = titles[0]["id"]

        logger.debug("Title ID was found: %s", title_id)
        return title_id

    async def get_title(self, title: str) -> dict:
        title_id = await self.get_title_id(title)
        return await self._request(HTTPMethod.GET, endpoint=f"titles/{title_id}")

    async def get_title_rating(self, title: str) -> tuple[float, float]:
        title_data = await self.get_title(title)

        rating = title_data.get("rating", {})
        metacritic_rating = title_data.get("metacritic", {})

        logger.debug("Found title info: %s", title_data)
        logger.debug("Title Rating: %s, %s", rating, metacritic_rating)

        return rating.get("aggregateRating"), metacritic_rating.get("score")
