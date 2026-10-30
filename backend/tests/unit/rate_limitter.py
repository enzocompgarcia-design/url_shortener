import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture
def user_payload():
    return {"long_link": "https://google.com"}


def test_rate_limiting(user_payload):
    first_response = client.post("/link", json=user_payload)

    assert first_response.status_code == status.HTTP_200_OK

    second_response = client.post("/link", json=user_payload)

    assert second_response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
