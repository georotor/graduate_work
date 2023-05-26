from redis.asyncio.client import Redis


redis: Redis | None = None


async def get_redis() -> Redis:
    """Функция для DI FastAPI."""
    return redis
