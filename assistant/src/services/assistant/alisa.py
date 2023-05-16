"""Реализация AbstractAssistant для Алисы."""
import logging
from functools import lru_cache

from fastapi import Depends

from models.alisa import AliceRequest, AliceResponse, Response
from services.assistant.abstract import AbstractAssistant

logger = logging.getLogger(__name__)


class Alisa(AbstractAssistant):
    """Реализация AbstractAssistant для Алисы."""

    async def handler(self, request: dict) -> dict:
        """Обработка входящего сообщения от Алисы."""
        alisa_request = AliceRequest.parse_obj(request)

        if "film_length" in alisa_request.request.nlu.intents:
            return await self._film_length(alisa_request)

        if "film_director" in alisa_request.request.nlu.intents:
            return await self._film_director(alisa_request)

        response = Response(text="Привет")
        alisa_response = AliceResponse(
            **alisa_request.dict(),
            response=response.dict(),
        )

        return alisa_response.dict()

    async def _film_director(self, request: AliceRequest) -> dict:
        """Обработка запроса 'Кто автор фильма'."""
        film = request.get_context("film_director")
        if not film:
            film = request.state.session.get("film")

        if not film:
            return await self._request_film_error(request)

        text = "Братья Вачовски, а ныне сёстры"

        response = Response(text=text)

        alisa_response = AliceResponse(
            **request.dict(),
            response=response.dict(),
            session_state={"film": film}
        )

        return alisa_response.dict()

    async def _film_length(self, request: AliceRequest) -> dict:
        """Обработка запроса 'Сколько длится фильм'."""
        film = request.get_context("film_length")
        if not film:
            film = request.state.session.get("film")

        if not film:
            return await self._request_film_error(request)

        text = "2 часа"

        response = Response(text=text)

        alisa_response = AliceResponse(
            **request.dict(),
            response=response.dict(),
            session_state={"film": film}
        )

        return alisa_response.dict()

    async def _request_film_error(self, request: AliceRequest) -> dict:
        response = Response(text="Пожалуйста, уточните вопрос")

        return AliceResponse(
            **request.dict(),
            response=response.dict()
        ).dict()


@lru_cache
def get_alisa() -> AbstractAssistant:
    """DI для FastAPI. Получаем менеджер для Алисы."""
    return Alisa()
