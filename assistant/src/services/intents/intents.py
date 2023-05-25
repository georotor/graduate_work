"""Модуля выделения намерений и сущностей."""
import aiohttp
import logging
from functools import lru_cache
from http import HTTPStatus

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
        nlu_data = None
        json = {"text": text}

        async with aiohttp.ClientSession() as client:
            try:
                nlu_data = await self._fetch(client, json)
            except aiohttp.ClientError as e:
                logger.error("NLU error: {0}".format(e))

        if nlu_data:
            return Intent(
                intent=nlu_data["intent"].get("name", ""),
                entities=nlu_data["entities"]
            )

    async def _fetch(self, client: aiohttp.ClientSession, json: dict) -> dict | None:
        """Отправка запроса на выделение намерения."""
        async with client.post(self.url, json=json) as response:
            if response.status == HTTPStatus.OK:
                nlu_data = await response.json()
                logger.info("Get data from NLU {0}".format(nlu_data))
                return nlu_data

            logger.error("Not get data from NLU for command {0}, {1}".format(
                json,
                await response.text()
            ))


@lru_cache
def get_intent_parse() -> AbstractIntents:
    """DI для FastAPI. Получаем менеджер для парсера намерений и сущностей."""
    return IntentParse(url=settings.nlu_model_parse)
