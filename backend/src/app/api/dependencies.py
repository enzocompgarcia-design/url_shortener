from fastapi import Depends
from redis import Redis

from app.database.cache.connections import get_cache
from app.repositories.link_repository import LinksRepository
from app.services.shorten_url_service import ShortenLinkService


def get_shorten_link_service(cache: Redis = Depends(get_cache)) -> ShortenLinkService:

    return ShortenLinkService(LinksRepository(cache=cache))
