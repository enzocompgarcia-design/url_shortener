import pytest

from app.errors.exceptions import InvalidLongLink, InvalidProtocol
from app.services.shortener_url_service import ShortenLinkService


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("https://example.com", "https://example.com"),
        ("http://example.com", "http://example.com"),
        ("example.com", "https://example.com"),
        ("  example.com  ", "https://example.com"),
    ],
)
def test_validate_valid_urls(url, expected):
    assert ShortenLinkService.validate_long_link(url) == expected


@pytest.mark.parametrize(
    ("url", "expected_exception"),
    [
        ("", InvalidLongLink),
        ("   ", InvalidLongLink),
        ("invalid url", InvalidLongLink),
        ("http://", InvalidLongLink),
        ("ftp://example.com", InvalidProtocol),
        ("javascript:alert(1)", InvalidLongLink),
        ("https://", InvalidLongLink),
        ("http://exa mple.com", InvalidLongLink),
    ],
)
def test_validate_invalid_urls(url, expected_exception):
    with pytest.raises(expected_exception):
        ShortenLinkService.validate_long_link(url)
