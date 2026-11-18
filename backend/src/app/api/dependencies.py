from fastapi import Depends
from redis import Redis

from app.database.cache.connections import get_cache
from app.repositories.link_repository import LinksRepository
from app.services.healthy_service import HealthyService
from app.services.shortener_url_service import ShortenLinkService


def get_shorten_link_service(cache: Redis = Depends(get_cache)) -> ShortenLinkService:

    return ShortenLinkService(LinksRepository(cache=cache))


def get_healthy_service(cache: Redis = Depends(get_cache)) -> HealthyService:
    return HealthyService(cache=cache)
