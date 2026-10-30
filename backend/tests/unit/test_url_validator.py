import pytest

from app.errors.exceptions import InvalidLongLink
from app.services.shorten_url_service import ShortenLinkService


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("https://example.com", "https://example.com"),
        ("http://example.com", "http://example.com"),
        ("example.com", "https://example.com"),
        ("ftp://example.com", "ftp://example.com"),
        ("  example.com  ", "https://example.com"),
    ],
)
def test_validate_valid_urls(url, expected):
    assert ShortenLinkService.validate_long_link(url) == expected


@pytest.mark.parametrize(
    "url",
    [
        "",
        "   ",
        "invalid url",
        "http://",
        "example.com:invalid",
    ],
)
def test_validate_invalid_urls(url):
    with pytest.raises(InvalidLongLink):
        ShortenLinkService.validate_long_link(url)
