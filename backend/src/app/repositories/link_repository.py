from redis import Redis
from starlette.concurrency import run_in_threadpool

from app.config import config
from app.database.cassandra.models import LinksTableDb
from app.errors.exceptions import LongLinkNotFound


class LinksRepository:
    def __init__(self, cache: Redis):
        self.cache = cache

    async def add_link(self, short_link: str, long_link: str):
        link = await run_in_threadpool(
            lambda: LinksTableDb.objects.ttl(
                config.CASSANDRA_TTL_10_YEARS
            ).create(
                short_link=short_link,
                long_link=long_link
            )
        )

        return link

    async def get_long_link(self, short_link: str):
        # Cache hit: skips the database query.
        long_link = await self.cache.get(short_link)

        if long_link:
            return long_link

        link = await run_in_threadpool(
            lambda: LinksTableDb.objects(short_link=short_link).first()
        )

        if link is None:
            raise LongLinkNotFound(short_link)

        await self.cache.set(short_link, link.long_link, ex=3600)
        return link.long_link
