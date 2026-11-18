from fastapi import status

from app.api.dependencies import get_healthy_service
from app.services import healthy_service as healthy_service_module
from app.services.healthy_service import HealthyService


class HealthyCache:
    async def ping(self):
        return True


class UnavailableCache:
    async def ping(self):
        raise ConnectionError("redis is down")


class HealthySession:
    def execute(self, query, timeout=None):
        return None


class UnavailableSession:
    def execute(self, query, timeout=None):
        raise RuntimeError("cassandra is down")


def _override_service(client, monkeypatch, *, cache, session):
    monkeypatch.setattr(healthy_service_module.connection, "session", session)
    client.app.dependency_overrides[get_healthy_service] = lambda: HealthyService(
        cache=cache
    )


def test_health_returns_ok(client):
    response = client.get("/health")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}


def test_ready_returns_ok_when_dependencies_are_available(client, monkeypatch):
    _override_service(
        client, monkeypatch, cache=HealthyCache(), session=HealthySession()
    )

    response = client.get("/ready")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}


def test_ready_returns_503_when_cache_is_unavailable(client, monkeypatch):
    _override_service(
        client, monkeypatch, cache=UnavailableCache(), session=HealthySession()
    )

    response = client.get("/ready")

    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert response.json() == {
        "detail": "Cache não responde",
        "error_code": "cache_unavailable",
    }


def test_ready_returns_503_when_cache_is_not_initialized(client, monkeypatch):
    _override_service(client, monkeypatch, cache=None, session=HealthySession())

    response = client.get("/ready")

    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert response.json() == {
        "detail": "Cache não inicializado",
        "error_code": "cache_unavailable",
    }


def test_ready_returns_503_when_database_is_unavailable(client, monkeypatch):
    _override_service(
        client, monkeypatch, cache=HealthyCache(), session=UnavailableSession()
    )

    response = client.get("/ready")

    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert response.json() == {
        "detail": "Banco de dados não responde",
        "error_code": "database_unavailable",
    }


def test_ready_returns_503_when_database_is_not_initialized(client, monkeypatch):
    _override_service(client, monkeypatch, cache=HealthyCache(), session=None)

    response = client.get("/ready")

    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert response.json() == {
        "detail": "Banco de dados não inicializado",
        "error_code": "database_unavailable",
    }
