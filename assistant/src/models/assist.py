import aiohttp
from fastapi import HTTPException, status
from pydantic import BaseModel


class AssistBaseModel(BaseModel):
    version: str
    session: dict


class Request(BaseModel):
    command: str


class State(BaseModel):
    session: dict


class AssistRequest(AssistBaseModel):
    intent: str | None = None
    entities: list | None = None
    request: Request
    state: State

    async def get_context(self, entity: str):
        if self.entities is None:
            await self.get_intent()

        for item in self.entities:
            if item.get("entity") == entity:
                return item.get("value")

        return None

    async def get_intent(self) -> str:
        if self.intent is not None:
            return self.intent

        self.intent = ""

        if self.request.command:
            session = aiohttp.ClientSession()
            headers = {'Content-Type': 'application/json'}
            json = {"text": self.request.command}
            async with session.post("http://localhost:5005/model/parse", json=json, headers=headers) as model_response:
                if model_response.status == status.HTTP_200_OK:
                    data = await model_response.json()
                    self.intent = data["intent"].get("name", "")
                    self.entities = data["entities"]

            await session.close()

        return self.intent


class Response(BaseModel):
    text: str
    end_session: bool = False


class AssistResponse(AssistBaseModel):
    response: Response
    session_state: dict = {}
