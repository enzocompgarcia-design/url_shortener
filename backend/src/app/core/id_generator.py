from hashids import Hashids
from redis import Redis

from app.config import config


class IDGenerator:
    def __init__(self, cache: Redis):
        self.cache = cache
        self.hashids = Hashids(salt=config.SECRET_KEY, alphabet=config.ALPHABET)

    def generate(self) -> str:
        return self.hashids.encode(self.cache.incr(config.NAME_CACHE_ID))
