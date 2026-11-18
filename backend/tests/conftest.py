import os
import sys
from pathlib import Path
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

# Ensure the app package is importable (backend/src)
BACKEND_SRC = Path(__file__).resolve().parents[1] / "src"
if str(BACKEND_SRC) not in sys.path:
    sys.path.insert(0, str(BACKEND_SRC))

# Minimal variables required to load app.config in the test environment
os.environ.setdefault("CASSANDRA_HOST", "localhost")
os.environ.setdefault("CASSANDRA_PORT", "9042")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault(
    "ALPHABET", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
)
os.environ.setdefault("NAME_CACHE_ID", "test:id")
os.environ.setdefault("ID_START", "1000")
os.environ.setdefault("ORIGINS", '["http://localhost:3000"]')
os.environ.setdefault("ALLOWED_PROTOCOLS", '["http","https"]')


@pytest.fixture
def fake_cache():
    class FakeCache:
        def __init__(self):
            self.store = {}

        async def get(self, key):
            return self.store.get(key)

        async def set(self, key, value, ex=None):
            self.store[key] = value
            return True

    return FakeCache()


@pytest.fixture
def fake_id_generator():
    class FakeIDGenerator:
        def __init__(self):
            self.counter = 0

        def generate(self):
            self.counter += 1
            return f"abc{self.counter}"

    return FakeIDGenerator()


@pytest.fixture
def mock_link_repository(monkeypatch):
    from app.repositories import link_repository as repo_module

    add_link = AsyncMock(return_value=None)
    get_long_link = AsyncMock(return_value="https://example.com")

    monkeypatch.setattr(repo_module.LinksRepository, "add_link", add_link)
    monkeypatch.setattr(repo_module.LinksRepository, "get_long_link", get_long_link)

    return {"add_link": add_link, "get_long_link": get_long_link}


@pytest.fixture
def client(monkeypatch, fake_cache, fake_id_generator, mock_link_repository):
    import app.database.cache.connections as cache_connections
    import app.database.cassandra.connections as cassandra_connections
    import app.main as main_module
    from app.api.dependencies import get_shorten_link_service
    from app.repositories.link_repository import LinksRepository
    from app.services.shortener_url_service import ShortenLinkService

    async def noop_async(*args, **kwargs):
        return None

    monkeypatch.setattr(cassandra_connections, "create_tables", lambda: None)
    monkeypatch.setattr(main_module, "create_tables", lambda: None)
    monkeypatch.setattr(cache_connections, "init_redis", noop_async)
    monkeypatch.setattr(cache_connections, "close_redis", noop_async)
    monkeypatch.setattr(main_module, "init_redis", noop_async)
    monkeypatch.setattr(main_module, "close_redis", noop_async)
    monkeypatch.setattr(cache_connections, "get_cache", lambda: fake_cache)
    monkeypatch.setattr(cache_connections, "get_id_generator", lambda: object())
    monkeypatch.setattr(main_module, "get_id_generator", lambda: object())

    app = main_module.app
    app.dependency_overrides[get_shorten_link_service] = lambda: ShortenLinkService(
        LinksRepository(cache=fake_cache)
    )

    # Avoids shared limiter state between tests
    if hasattr(app.state, "limiter") and hasattr(app.state.limiter, "_storage"):
        try:
            app.state.limiter._storage.reset()
        except Exception:
            pass

    with TestClient(app) as test_client:
        app.state.id_generator = fake_id_generator
        yield test_client

    app.dependency_overrides.clear()
