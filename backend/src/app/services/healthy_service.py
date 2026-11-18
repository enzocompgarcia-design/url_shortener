import asyncio

from cassandra.cqlengine import connection
from redis.asyncio import Redis
from starlette.concurrency import run_in_threadpool

from app.config import config
from app.errors.exceptions import CacheUnavailable, DatabaseUnavailable

DATABASE_CHECK_QUERY = "SELECT release_version FROM system.local"


class HealthyService:
    def __init__(self, cache: Redis):
        self.cache = cache

    def health(self) -> dict[str, str]:
        return {"status": "ok"}

    async def ready(self) -> dict[str, str]:
        await asyncio.gather(
            self._check_cache(),
            self._check_database(),
        )

        return {"status": "ok"}

    async def _check_cache(self) -> None:
        if self.cache is None:
            raise CacheUnavailable("Cache não inicializado")

        try:
            await asyncio.wait_for(
                self.cache.ping(), timeout=config.CACHE_CHECK_TIMEOUT
            )
        except Exception as exc:
            raise CacheUnavailable("Cache não responde") from exc

    def _check_database_sync(self) -> None:
        session = getattr(connection, "session", None)
        if session is None:
            raise DatabaseUnavailable("Banco de dados não inicializado")

        try:
            session.execute(DATABASE_CHECK_QUERY, timeout=config.DATABASE_CHECK_TIMEOUT)
        except Exception as exc:
            raise DatabaseUnavailable("Banco de dados não responde") from exc

    async def _check_database(self) -> None:
        await run_in_threadpool(self._check_database_sync)
