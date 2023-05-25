from pydantic import BaseModel


class Entity(BaseModel):
    entity: str
    value: str


class Intent(BaseModel):
    intent: str = ""
    entities: list[Entity] | list
