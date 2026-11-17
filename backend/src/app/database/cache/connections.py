import redis
import redis.asyncio as async_redis

from app.config import config

sync_redis: redis.Redis | None = None
async_cache: async_redis.Redis | None = None


def get_cache():
    return async_cache


def get_id_generator():
    return sync_redis


async def init_redis() -> None:
    global sync_redis, async_cache

    sync_redis = redis.Redis.from_url(
        config.REDIS_URL,
        decode_responses=True,
    )
    sync_redis.set(
        config.NAME_CACHE_ID,
        config.ID_START,
        nx=True,
    )

    async_cache = async_redis.Redis.from_url(
        config.REDIS_URL,
        decode_responses=True,
    )


async def close_redis() -> None:
    global sync_redis, async_cache

    if async_cache is not None:
        await async_cache.aclose()
        async_cache = None

    if sync_redis is not None:
        sync_redis.close()
        sync_redis = None
