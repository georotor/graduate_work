"""Описание интерфейса для работы с помощниками."""
from abc import ABC, abstractmethod


class AbstractAssistant(ABC):
    """Менеджер для работы с помощниками."""

    @abstractmethod
    async def handler(self, request: dict) -> dict:
        """Обработка сообщения пользователя."""
