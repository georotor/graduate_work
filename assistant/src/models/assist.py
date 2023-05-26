from pydantic import BaseModel


class AssistBaseModel(BaseModel):
    version: str
    session: dict


class NLU(BaseModel):
    tokens: list = []
    entities: list = []
    intents: dict = {}


class Request(BaseModel):
    command: str
    nlu: NLU


class State(BaseModel):
    session: dict


class AssistRequest(AssistBaseModel):
    intent: str = ""
    entities: list = []
    request: Request
    state: State

    async def get_entity(self, entity: str) -> str | None:
        for item in self.entities:
            if item.entity == entity:
                return item.value

        return None


class Response(BaseModel):
    text: str
    end_session: bool = False


class AssistResponse(AssistBaseModel):
    response: Response
    session_state: dict = {}
