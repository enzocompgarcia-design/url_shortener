from hashids import Hashids
from redis import Redis
from redis.exceptions import RedisError

from app.config import config
from app.errors.exceptions import CacheUnavailable


class IDGenerator:
    def __init__(self, cache: Redis):
        if cache is None:
            raise CacheUnavailable("Cache não inicializado")

        self.cache = cache
        self.hashids = Hashids(salt=config.SECRET_KEY, alphabet=config.ALPHABET)

    def generate(self) -> str:
        try:
            next_id = self.cache.incr(config.NAME_CACHE_ID)
        except RedisError as exc:
            raise CacheUnavailable() from exc

        return self.hashids.encode(next_id)
