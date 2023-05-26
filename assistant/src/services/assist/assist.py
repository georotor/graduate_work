"""Интерфейс для работы с помощниками."""
import logging
from functools import lru_cache

from .abstract import AbstractAssist
from .dialogs import dialogs
from core.config import settings
from models.assist import AssistRequest, AssistResponse
from models.intents import Entity
from services.content import AbstractContent, Content
from services.intents import AbstractIntents, IntentParse

logger = logging.getLogger(__name__)


class Assist(AbstractAssist):
    """Реализация AbstractAssistant для Алисы и Маруси."""

    def __init__(self, intent_parse: AbstractIntents, content: AbstractContent):
        self.intent_parse = intent_parse
        self.content = content

    async def handler(self, request: AssistRequest) -> AssistResponse:
        """Обработка входящего сообщения от ассистента."""
        logger.info("Get request {0}".format(request))

        await self._get_intent(request)
        current_dialog = request.state.session.get("dialog", "Welcome")
        logger.info("Dialog {0}".format(current_dialog))

        dialog = dialogs.get(current_dialog)(content=self.content)
        response = await dialog.handler(request)
        logger.info("Send response {0}".format(response))

        return response

    async def _get_intent(self, request: AssistRequest):
        """Выделение намерения из текстового сообщения."""
        if request.request.nlu.intents.keys():
            await self._get_intent_from_request(request)
            return

        await self._get_intent_from_model(request)

    @staticmethod
    async def _get_intent_from_request(request: AssistRequest):
        """Выделение намерения из запроса помощника."""
        if not request.request.nlu.intents.keys():
            return

        intent = next(iter(request.request.nlu.intents))
        entities = []

        for entity_name, entity_data in request.request.nlu.intents[intent].get("slots", {}).items():
            entities.append(Entity(entity=entity_name, value=entity_data.get("value")))

        request.intent = intent
        request.entities = entities

    async def _get_intent_from_model(self, request: AssistRequest):
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
    content = Content()

    return Assist(intent_parse=intent_parse, content=content)
