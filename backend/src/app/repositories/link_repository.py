from cassandra import DriverException
from cassandra.cqlengine.connection import CQLEngineException
from redis import Redis
from redis.exceptions import RedisError
from starlette.concurrency import run_in_threadpool

from app.config import config
from app.database.cassandra.models import LinksTableDb
from app.errors.exceptions import (
    CacheUnavailable,
    DatabaseUnavailable,
    LongLinkNotFound,
)

DATABASE_ERRORS = (DriverException, CQLEngineException)


class LinksRepository:
    def __init__(self, cache: Redis):
        self.cache = cache

    async def add_link(self, short_link: str, long_link: str):
        try:
            return await run_in_threadpool(
                lambda: LinksTableDb.objects.ttl(
                    config.CASSANDRA_TTL_10_YEARS
                ).create(
                    short_link=short_link,
                    long_link=long_link
                )
            )
        except DATABASE_ERRORS as exc:
            raise DatabaseUnavailable() from exc

    async def get_long_link(self, short_link: str):
        # Cache hit: skips the database query.
        long_link = await self._get_cached_long_link(short_link)

        if long_link:
            return long_link

        try:
            link = await run_in_threadpool(
                lambda: LinksTableDb.objects(short_link=short_link).first()
            )
        except DATABASE_ERRORS as exc:
            raise DatabaseUnavailable() from exc

        if link is None:
            raise LongLinkNotFound(short_link)

        await self._set_cached_long_link(short_link, link.long_link)
        return link.long_link

    async def _get_cached_long_link(self, short_link: str):
        if self.cache is None:
            raise CacheUnavailable("Cache não inicializado")

        try:
            return await self.cache.get(short_link)
        except RedisError as exc:
            raise CacheUnavailable() from exc

    async def _set_cached_long_link(self, short_link: str, long_link: str) -> None:
        if self.cache is None:
            raise CacheUnavailable("Cache não inicializado")

        try:
            await self.cache.set(short_link, long_link, ex=3600)
        except RedisError as exc:
            raise CacheUnavailable() from exc
