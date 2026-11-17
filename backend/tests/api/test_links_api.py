from fastapi import status


def test_create_short_link_returns_short_url(client, mock_link_repository):
    payload = {"long_link": "https://example.com"}

    response = client.post("/link/", json=payload)

    print(response.json())
    assert response.status_code == status.HTTP_200_OK
    mock_link_repository["add_link"].assert_awaited_once()


def test_create_short_link_rejects_invalid_protocol(client):
    payload = {"long_link": "ftp://example.com"}

    response = client.post("/link/", json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    body = response.json()
    assert body["error_code"] == "invalid_long_link"


def test_redirect_link_returns_long_url(client, mock_link_repository):
    mock_link_repository["get_long_link"].return_value = "https://destino.com"

    response = client.get("/link/abc123", follow_redirects=False)

    assert response.status_code == status.HTTP_301_MOVED_PERMANENTLY
    assert response.headers["location"] == "https://destino.com"


def test_redirect_link_not_found(client, monkeypatch):
    from app.api.dependencies import get_shorten_link_service
    from app.errors.exceptions import LongLinkNotFound

    async def raise_not_found(*args, **kwargs):
        raise LongLinkNotFound("inexistente")

    class FakeService:
        async def redirect_link(self, short_link: str):
            await raise_not_found(short_link)

    client.app.dependency_overrides[get_shorten_link_service] = lambda: FakeService()

    response = client.get("/link/inexistente")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    body = response.json()
    assert body["error_code"] == "long_link_not_found"
