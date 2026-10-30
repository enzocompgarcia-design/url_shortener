import redis
import redis.asyncio as async_redis

from app.config import config


def get_cache():
    return async_cache


def get_id_generator():
    return sync_redis


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
