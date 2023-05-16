from pydantic import BaseModel


class AliceaBaseModel(BaseModel):
    version: str
    session: dict


class NLU(BaseModel):
    tokens: list
    entities: list
    intents: dict


class Request(BaseModel):
    command: str
    nlu: NLU


class State(BaseModel):
    session: dict


class AliceRequest(AliceaBaseModel):
    request: Request
    state: State

    def get_context(self, intent: str):
        what = self.request.nlu.intents[intent]["slots"].get("what")
        if not what:
            return None

        if "value" in what:
            return str(what["value"])

        return None

    def get_intent(self) -> str | None:
        if self.request.nlu.intents.keys():
            return next(iter(self.request.nlu.intents))

        return None


class Response(BaseModel):
    text: str
    end_session: bool = False


class AliceResponse(AliceaBaseModel):
    response: Response
    session_state: dict = {}
