"""Интерфейс для работы с помощниками."""
import logging
from functools import lru_cache

from .abstract import AbstractAssist
from .dialogs import dialogs
from core.config import settings
from models.assist import AssistRequest, AssistResponse
from services.intents.abstarct import AbstractIntents
from services.intents import IntentParse

logger = logging.getLogger(__name__)


class Assist(AbstractAssist):
    """Реализация AbstractAssistant для Алисы и Маруси."""

    def __init__(self, intent_parse: AbstractIntents):
        self.intent_parse = intent_parse

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

        intent = await self.intent_parse.parse(request.request.command)
        if intent:
            request.intent = intent.intent
            request.entities = intent.entities


@lru_cache
def get_assist() -> AbstractAssist:
    """DI для FastAPI. Получаем менеджер для ассистента."""
    intent_parse = IntentParse(url=settings.nlu_model_parse)
    return Assist(intent_parse=intent_parse)
