from fastapi import status


def _override_service(client, service):
    from app.api.dependencies import get_shorten_link_service

    client.app.dependency_overrides[get_shorten_link_service] = lambda: service


def test_cache_unavailable_maps_to_503(client):
    from app.errors.exceptions import CacheUnavailable

    class FailingService:
        async def redirect_link(self, short_link: str):
            raise CacheUnavailable()

    _override_service(client, FailingService())

    response = client.get("/link/abc123")

    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert response.json() == {
        "detail": "Cache indisponível",
        "error_code": "cache_unavailable",
    }


def test_database_unavailable_maps_to_503(client):
    from app.errors.exceptions import DatabaseUnavailable

    class FailingService:
        async def redirect_link(self, short_link: str):
            raise DatabaseUnavailable()

    _override_service(client, FailingService())

    response = client.get("/link/abc123")

    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert response.json() == {
        "detail": "Banco de dados indisponível",
        "error_code": "database_unavailable",
    }
