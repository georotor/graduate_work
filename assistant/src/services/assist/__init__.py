"""Описание интерфейса для работы с помощниками."""
import logging
from abc import ABC, abstractmethod
from functools import lru_cache

from .dialogs import dialogs
from models.assist import AssistRequest, AssistResponse

logger = logging.getLogger(__name__)


class AbstractAssist(ABC):
    """Менеджер для работы с помощниками."""

    @abstractmethod
    async def handler(self, request: AssistRequest) -> AssistResponse:
        """Обработка сообщения пользователя."""


class Assist(AbstractAssist):
    """Реализация AbstractAssistant для Алисы и Маруси."""

    async def handler(self, request: AssistRequest) -> AssistResponse:
        """Обработка входящего сообщения от ассистента."""
        current_dialog = request.state.session.get("dialog", "Welcome")

        dialog = dialogs.get(current_dialog)()
        response = await dialog.handler(request)

        return response


@lru_cache
def get_assist() -> AbstractAssist:
    """DI для FastAPI. Получаем менеджер для ассистента."""
    return Assist()
