"""API взаимодействия с голосовыми помощниками."""

from logging import config as logging_config

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import alisa
from core.config import settings
from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


app.include_router(alisa.router, prefix='/api/v1/alisa', tags=['alisa'])

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=False)
