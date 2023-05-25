"""Описание интерфейса модуля выделения намерений и сущностей."""
from abc import ABC, abstractmethod

from models.intents import Intent


class AbstractIntents(ABC):
    """Интерфейс выделения намерений и сущностей."""

    @abstractmethod
    async def parse(self, text: str) -> Intent | None:
        """Обработка сообщения."""
