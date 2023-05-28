"""Модуля выделения намерений и сущностей."""
import aiohttp
import logging
from functools import lru_cache
from http import HTTPStatus

from fastapi_cache.decorator import cache

from .abstarct import AbstractIntents
from core.config import settings
from models.intents import Intent

logger = logging.getLogger(__name__)


class IntentParse(AbstractIntents):
    """Интерфейс выделения намерений и сущностей."""

    def __init__(self, url: str):
        self.url = url

    async def parse(self, text: str) -> Intent | None:
        """Поиск намерения и сущности в сообщении."""
        json = {"text": text}
        nlu_data = await self._fetch(self.url, json)

        if nlu_data:
            return Intent(
                intent=nlu_data["intent"].get("name", ""),
                entities=nlu_data["entities"]
            )

        return None

    @staticmethod
    @cache()
    async def _fetch(url: str, json: dict) -> dict | None:
        """Отправка запроса на выделение намерения с кэшированием."""
        async with aiohttp.ClientSession() as client:
            try:
                async with client.post(url, json=json) as response:
                    if response.status == HTTPStatus.OK:
                        nlu_data = await response.json()
                        logger.info("Get data from NLU %s", nlu_data)
                        return nlu_data

                    logger.error("Not get data from NLU for command %s, %s", json, await response.text())
            except aiohttp.ClientError as e:
                logger.error("NLU error: %s", e)

        return None


@lru_cache
def get_intent_parse() -> AbstractIntents:
    """DI для FastAPI. Получаем менеджер для парсера намерений и сущностей."""
    return IntentParse(url=settings.nlu_model_parse)
