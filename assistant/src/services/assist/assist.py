"""Интерфейс для работы с помощниками."""
import aiohttp
import logging
from functools import lru_cache
from http import HTTPStatus

from .abstract import AbstractAssist
from .dialogs import dialogs
from core.config import settings
from models.assist import AssistRequest, AssistResponse

logger = logging.getLogger(__name__)


class Assist(AbstractAssist):
    """Реализация AbstractAssistant для Алисы и Маруси."""

    async def handler(self, request: AssistRequest) -> AssistResponse:
        """Обработка входящего сообщения от ассистента."""
        logger.info("Get request {0}".format(request))
        await self._get_intent(request)
        current_dialog = request.state.session.get("dialog", "Welcome")

        dialog = dialogs.get(current_dialog)()
        response = await dialog.handler(request)
        logger.info("Send response {0}".format(response))

        return response

    async def _get_intent(self, request: AssistRequest):
        """Выделение намерения из текстового сообщения."""
        if not request.request.command:
            return

        nlu_data = None
        json = {"text": request.request.command}

        async with aiohttp.ClientSession() as client:
            try:
                nlu_data = await self._request_intent(client, json)
            except aiohttp.ClientError as e:
                logger.error("NLU error: {0}".format(e))

        if nlu_data:
            request.intent = nlu_data["intent"].get("name", "")
            request.entities = nlu_data["entities"]

    @staticmethod
    async def _request_intent(client: aiohttp.ClientSession, json: dict) -> dict | None:
        """Отправка запроса на выделение намерения."""
        async with client.post(settings.nlu_model_parse, json=json) as response:
            if response.status == HTTPStatus.OK:
                nlu_data = await response.json()
                logger.info("Get data from NLU {0}".format(nlu_data))
                return nlu_data

            logger.error("Not get data from NLU for command {0}, {1}".format(
                json,
                await response.text()
            ))


@lru_cache
def get_assist() -> AbstractAssist:
    """DI для FastAPI. Получаем менеджер для ассистента."""
    return Assist()
