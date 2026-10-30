from fastapi import Depends
from redis import Redis
from sqlalchemy.orm import Session

from app.database.cache.connections import get_cache
from app.database.cassandra.connections import get_db
from app.repositories.link_repository import LinksRepository
from app.services.shorten_url_service import ShortenLinkService


def get_shorten_link_service(
    db: Session = Depends(get_db), cache: Redis = Depends(get_cache)
) -> ShortenLinkService:

    return ShortenLinkService(LinksRepository(db=db, cache=cache))
