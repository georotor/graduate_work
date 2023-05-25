import aiohttp
import logging
from dataclasses import dataclass
from functools import lru_cache
from http import HTTPStatus

from .abstract import AbstractContent
from core.config import settings
from models.content import Film

logger = logging.getLogger(__name__)


@dataclass
class HTTPResponse:
    body: dict
    status: int


class Content(AbstractContent):
    async def get_film(self, name: str) -> Film | None:
        films = await self.search_film(name)

        if not films:
            return None

        url = settings.content_film_get + films[0].get("id")
        http_result = await self._fetch(url=url)

        if http_result and http_result.status == HTTPStatus.OK:
            return Film(**http_result.body)

        return None

    async def search_film(self, name: str) -> list[dict]:
        films = []

        http_result = await self._fetch(
            url=settings.content_films_search,
            params={"query": name}
        )
        if http_result and http_result.status == HTTPStatus.OK:
            films = http_result.body.get("results", [])

        return films

    @staticmethod
    async def _fetch(url: str, params: dict | None = None,
                     json: dict | None = None, method: str = 'GET') -> HTTPResponse | None:
        """Отправка HTTP запроса."""
        params = params or {}
        json = json or {}

        async with aiohttp.ClientSession() as client:
            try:
                async with client.request(method, url, params=params, json=json) as response:
                    logger.info("HTTP {0} request: url={1} params={2} json={3}".format(
                        method, url, params, json
                    ))
                    return HTTPResponse(
                        body=await response.json(),
                        status=response.status,
                    )
            except aiohttp.ClientError as e:
                logger.error("Async API error: {0}".format(e))


@lru_cache
def get_content() -> AbstractContent:
    """DI для FastAPI."""
    return Content()
