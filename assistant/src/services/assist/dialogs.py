import inspect
import logging
import sys

from .messages import Message
from models.assist import AssistRequest, AssistResponse, Response
from services.content import AbstractContent

logger = logging.getLogger(__name__)


class BaseDialog:
    """Базовый класс диалога с помощником."""

    commands: {}

    def __init__(self, content: AbstractContent):
        self.content = content

    @classmethod
    def get_name(cls):
        return cls.__name__

    async def make_response(self, request: AssistRequest, text: str, state: dict | None = None) -> AssistResponse:
        """Подготовка ответа на запрос."""
        state = state or {}
        response = Response(text=text.strip())

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
        """Обработка входящего запроса."""
        command = self.commands.get(request.intent)
        if command:
            return await command(request)

        return await self.error(request)

    async def error(self, request: AssistRequest):
        """Отправка сообщения об ошибке."""
        return await self.make_response(request, Message.ERROR)


class Welcome(BaseDialog):
    """Начальный диалог с помощником."""

    def __init__(self, *args, **kwargs):
        self.commands = {
            "help": self.help,
            "film_length": self.film_length,
            "film_director": self.film_director,
        }
        super().__init__(*args, **kwargs)

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
        film_name = await request.get_entity("film")
        if not film_name:
            film_name = request.state.session.get("film")

        if not film_name:
            logger.error("Not found film name in dialog film_length {0}".format(request))
            return await self.error(request)

        logger.info("Find film name {0} in request {1}".format(film_name, request))

        film_data = await self.content.get_film(film_name)
        if not film_data:
            logger.warning("Not found film: {0}".format(film_name))
            return await self.make_response(request=request, text=Message.FILM_NOT_FOUND.format(film_name))

        if not bool(film_data.length):
            logger.warning("Not found length for film {0} in data {1}".format(film_name, film_data))
            return await self.make_response(
                request=request,
                text=Message.FILM_NOT_DATA.format(film_data.title),
                state={"film": film_name},
            )

        length = []
        hours = int(film_data.length/60/60)
        if hours > 0:
            length.append(await self._film_length_format(hours, 'hours'))

        minutes = int(film_data.length/60 - hours*60)
        if minutes > 0:
            length.append(await self._film_length_format(minutes, 'minutes'))

        return await self.make_response(
            request=request,
            text=Message.FILM_LENGTH.format(film_data.title, ' '.join(length)),
            state={"film": film_name},
        )

    @staticmethod
    async def _film_length_format(numeric: int, type_time: str = 'minutes') -> str:
        """Форматирование длительность кинопроизведения."""
        formats = {
            "minutes": ((5, "{0} минут"), (2, "{0} минуты"), (1, "{0} минута")),
            "hours": ((5, "{0} часов"), (2, "{0} часа"), (1, "{0} час")),
        }
        for number, template in formats[type_time]:
            if numeric >= number:
                return template.format(numeric)

    async def film_director(self, request: AssistRequest):
        """Обработка запроса 'Кто режиссер'."""
        film_name = await request.get_entity("film")
        if not film_name:
            film_name = request.state.session.get("film")

        if not film_name:
            logger.error("Not found film name in dialog film_director {0}".format(request))
            return await self.error(request)

        film_data = await self.content.get_film(film_name)
        if not film_data:
            logger.warning("Not found film: {0}".format(film_name))
            return await self.make_response(request=request, text=Message.FILM_NOT_FOUND.format(film_name))

        if not film_data.directors:
            logger.warning("Not found directors for film {0} in data {1}".format(film_name, film_data))
            return await self.make_response(
                request=request,
                text=Message.FILM_NOT_DATA.format(film_data.title),
                state={"film": film_name},
            )

        names = [film.name for film in film_data.directors]

        text = Message.FILM_DIRECTOR.format(film_data.title, names[0])
        if len(names) > 1:
            names_text = "{0} и {1}".format(", ".join(names[0:-1]), names[-1])
            text = Message.FILM_DIRECTORS.format(film_data.title, names_text)

        return await self.make_response(
            request=request,
            text=text,
            state={"film": film_name},
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
