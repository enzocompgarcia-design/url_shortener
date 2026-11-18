import asyncio

import pytest
from cassandra import DriverException
from cassandra.cqlengine.connection import CQLEngineException
from redis.exceptions import ConnectionError as RedisConnectionError

from app.core.id_generator import IDGenerator
from app.errors.exceptions import CacheUnavailable, DatabaseUnavailable
from app.repositories import link_repository as repo_module
from app.repositories.link_repository import LinksRepository


class FailingCache:
    async def get(self, key):
        raise RedisConnectionError("cache is down")

    async def set(self, key, value, ex=None):
        raise RedisConnectionError("cache is down")

    def incr(self, key):
        raise RedisConnectionError("cache is down")


class EmptyCache:
    async def get(self, key):
        return None


def test_id_generator_raises_cache_unavailable_when_incr_fails():
    generator = IDGenerator(cache=FailingCache())

    with pytest.raises(CacheUnavailable):
        generator.generate()


def test_id_generator_rejects_missing_cache():
    with pytest.raises(CacheUnavailable):
        IDGenerator(cache=None)


def test_repository_raises_cache_unavailable_when_cache_read_fails():
    repository = LinksRepository(cache=FailingCache())

    with pytest.raises(CacheUnavailable):
        asyncio.run(repository.get_long_link("abc123"))


def test_repository_raises_database_unavailable_when_write_fails(monkeypatch):
    async def failing_threadpool(*args, **kwargs):
        raise DriverException("database is down")

    monkeypatch.setattr(repo_module, "run_in_threadpool", failing_threadpool)
    repository = LinksRepository(cache=FailingCache())

    with pytest.raises(DatabaseUnavailable):
        asyncio.run(repository.add_link("abc123", "https://example.com"))


def test_repository_raises_database_unavailable_when_read_fails(monkeypatch):
    async def failing_threadpool(*args, **kwargs):
        raise DriverException("database is down")

    monkeypatch.setattr(repo_module, "run_in_threadpool", failing_threadpool)
    repository = LinksRepository(cache=EmptyCache())

    with pytest.raises(DatabaseUnavailable):
        asyncio.run(repository.get_long_link("abc123"))


def test_repository_raises_database_unavailable_for_cqlengine_errors(monkeypatch):
    async def failing_threadpool(*args, **kwargs):
        raise CQLEngineException("connection is not configured")

    monkeypatch.setattr(repo_module, "run_in_threadpool", failing_threadpool)
    repository = LinksRepository(cache=EmptyCache())

    with pytest.raises(DatabaseUnavailable):
        asyncio.run(repository.get_long_link("abc123"))
