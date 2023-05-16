"""Реализация AbstractAssistant для Алисы."""
import logging
from functools import lru_cache

from .dialogs import dialogs
from models.alisa import AliceRequest
from services.assistant.abstract import AbstractAssistant

logger = logging.getLogger(__name__)


class Alisa(AbstractAssistant):
    """Реализация AbstractAssistant для Алисы."""

    async def handler(self, request: dict) -> dict:
        """Обработка входящего сообщения от Алисы."""
        alisa_request = AliceRequest.parse_obj(request)

        current_scene = alisa_request.state.session.get("dialog", "Welcome")

        dialog = dialogs.get(current_scene)()
        response = await dialog.handler(alisa_request)

        return response.dict()


@lru_cache
def get_alisa() -> AbstractAssistant:
    """DI для FastAPI. Получаем менеджер для Алисы."""
    return Alisa()
