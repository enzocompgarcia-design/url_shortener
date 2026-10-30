from urllib.parse import urlparse

import tldextract

from app.database.cassandra.models import LinksTableDb
from app.errors.exceptions import InvalidLongLink
from app.repositories.link_repository import LinksRepository


class ShortenLinkService:
    def __init__(
        self,
        link_repository: LinksRepository,
    ):
        self.link_repository = link_repository

    async def shorten_link(
        self,
        actual_url,
        short_link,
        request,
    ) -> LinksTableDb:

        request.long_link = ShortenLinkService.validate_long_link(request.long_link)

        await self.link_repository.add_link(short_link=short_link, long_link=request.long_link)

        short_link = actual_url + str(short_link)

        return short_link

    async def redirect_link(self, short_link: str):
        return await self.link_repository.get_long_link(short_link)

    @staticmethod
    def validate_long_link(link_original: str) -> str:
        link = link_original.strip()

        if not link or any(char.isspace() for char in link):
            raise InvalidLongLink(link)

        if "://" not in link:
            link = f"https://{link}"

        try:
            url = urlparse(link)

            if not url.hostname:
                raise InvalidLongLink(link)

            _ = url.port

        except ValueError as exc:
            raise InvalidLongLink(link_original) from exc

        extracted = tldextract.extract(url.hostname)

        if not (extracted.domain and extracted.suffix):
            raise InvalidLongLink(link)

        return link
