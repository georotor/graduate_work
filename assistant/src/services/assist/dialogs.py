import inspect
import sys

from .messages import Message
from models.assist import AssistRequest, AssistResponse, Response


class BaseDialog:
    """Базовый класс диалога с Алисой."""

    commands: {}

    @classmethod
    def get_name(cls):
        return cls.__name__

    async def make_response(self, request: AssistRequest, text: str, state: dict | None = None) -> AssistResponse:
        state = state or {}
        response = Response(text=text)

        alisa_response = AssistResponse(
            **request.dict(),
            response=response.dict(),
            session_state={
                "dialog": self.get_name(),
                **state
            },
        )

        return alisa_response

    async def handler(self, request: AssistRequest):
        intent = await request.get_intent()
        command = self.commands.get(intent)
        if command:
            return await command(request)

        return await self.error(request)

    async def error(self, request: AssistRequest):
        return await self.make_response(request, Message.ERROR)


class Welcome(BaseDialog):
    """Начальный диалог с Алисой."""

    def __init__(self):
        self.commands = {
            "help": self.help,
            "film_length": self.film_length,
            "film_director": self.film_director,
        }

    async def handler(self, request: AssistRequest) -> AssistResponse:
        """Если это новая сессия отправляем приветствие, иначе обрабатываем сообщение."""
        if request.session.get("new"):
            return await self.make_response(request, Message.WELCOME)

        return await super().handler(request)

    async def help(self, request: AssistRequest):
        """Отправка справочного сообщения."""
        return await self.make_response(request, Message.HELP)

    async def film_length(self, request: AssistRequest):
        """Обработка запроса 'Сколько длится фильм'."""
        film = await request.get_context("film")
        if not film:
            film = request.state.session.get("film")

        if not film:
            return await self.error(request)

        text = "2 часа"

        return await self.make_response(
            request=request,
            text=text,
            state={"film": film},
        )

    async def film_director(self, request: AssistRequest):
        """Обработка запроса 'Кто режиссер'."""
        film = await request.get_context("film")
        if not film:
            film = request.state.session.get("film")

        if not film:
            return await self.error(request)

        text = "Братья Вачовски, а ныне сёстры"

        return await self.make_response(
            request=request,
            text=text,
            state={"film": film},
        )


def get_dialogs():
    _dialogs = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj) and issubclass(obj, BaseDialog):
            _dialogs.append(obj)
    return _dialogs


dialogs = {
    dialog.get_name(): dialog for dialog in get_dialogs()
}
