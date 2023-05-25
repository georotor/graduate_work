"""Описание интерфейса получения данных кинопроизведений."""
from abc import ABC, abstractmethod

from models.content import Film


class AbstractContent(ABC):
    """Интерфейс получения данных кинопроизведений."""

    @abstractmethod
    async def get_film(self, name: str) -> Film | None:
        """Получение данных кинопроизведения."""
