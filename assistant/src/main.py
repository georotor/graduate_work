"""API взаимодействия с голосовыми помощниками."""

from logging import config as logging_config

import uvicorn
import redis.asyncio as aioredis
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from api.v1 import alisa, marusia
from db import redis
from core.config import settings
from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    redis.redis = await aioredis.from_url(
        "redis://{0}:{1}".format(settings.redis_host, settings.redis_port),
        encoding="utf8",
        decode_responses=True,
        max_connections=20,
    )
    FastAPICache.init(
        RedisBackend(redis.redis),
        prefix="cache:assist",
        expire=settings.cache_expire
    )


@app.on_event("shutdown")
async def shutdown():
    await redis.redis.close()


app.include_router(alisa.router, prefix='/api/v1/alisa', tags=['alisa'])
app.include_router(marusia.router, prefix='/api/v1/marusia', tags=['marusia'])


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=False)
