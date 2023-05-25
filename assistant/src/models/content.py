from uuid import UUID

from pydantic import BaseModel


class Genre(BaseModel):
    id: UUID
    name: str


class Person(BaseModel):
    id: UUID
    name: str


class Film(BaseModel):
    id: UUID
    title: str
    imdb_rating: float
    length: int
    description: str = ""
    genre: list[Genre]
    actors: list[Person]
    writers: list[Person]
    directors: list[Person]
