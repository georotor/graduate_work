"""Описание интерфейса для работы с помощниками."""
from abc import ABC, abstractmethod

from models.assist import AssistRequest, AssistResponse


class AbstractAssist(ABC):
    """Менеджер для работы с помощниками."""

    @abstractmethod
    async def handler(self, request: AssistRequest) -> AssistResponse:
        """Обработка сообщения пользователя."""
