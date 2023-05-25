"""Настройки приложения."""

from pydantic import BaseModel, BaseSettings


class Logging(BaseModel):
    """Настройки уровней логирования."""

    level_root: str = 'INFO'
    level_uvicorn: str = 'INFO'
    level_console: str = 'DEBUG'


class Settings(BaseSettings):
    """Настройки приложения."""

    project_name: str = 'assistant'

    nlu_model_parse: str = 'http://localhost:5005/model/parse'

    content_films_search: str = 'http://localhost/api/v1/films/search'
    content_film_get: str = 'http://localhost/api/v1/films/'

    logging: Logging = Logging()

    class Config:
        env_nested_delimiter = '__'


settings = Settings()
