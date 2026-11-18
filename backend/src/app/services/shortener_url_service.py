from urllib.parse import urlparse

import tldextract

from app.config import config
from app.errors.exceptions import InvalidLongLink, InvalidProtocol
from app.repositories.link_repository import LinksRepository


class ShortenLinkService:
    def __init__(
        self,
        link_repository: LinksRepository,
    ):
        self.link_repository = link_repository

    async def shorten_link(
        self,
        short_link,
        long_link,
    ) -> str:

        long_link = ShortenLinkService.validate_long_link(long_link)

        await self.link_repository.add_link(short_link=short_link, long_link=long_link)

        return str(short_link)

    async def redirect_link(self, short_link: str):
        return await self.link_repository.get_long_link(short_link)

    @staticmethod
    def validate_long_link(link_original: str) -> str:
        link = link_original.strip()

        if not link or any(char.isspace() for char in link):
            raise InvalidLongLink(link_original)

        if "://" in link:
            scheme = urlparse(link).scheme.lower()

            if scheme not in config.ALLOWED_PROTOCOLS:
                raise InvalidProtocol(scheme)
        else:
            link = f"{config.DEFAULT_PROTOCOL}://{link}"

        try:
            url = urlparse(link)

            if not url.hostname:
                raise InvalidLongLink(link_original)

            _ = url.port

        except ValueError as exc:
            raise InvalidLongLink(link_original) from exc

        extracted = tldextract.extract(url.hostname)

        if not (extracted.domain and extracted.suffix):
            raise InvalidLongLink(link_original)

        return link
