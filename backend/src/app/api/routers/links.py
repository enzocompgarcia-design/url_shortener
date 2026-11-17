from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.api.dependencies import get_shorten_link_service
from app.schemas.links import CreatShortLinkRequest, CreatShortLinkResponse
from app.services.shorten_url_service import ShortenLinkService

shorten_link_router = APIRouter(prefix="/link")

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],
)


@shorten_link_router.post("/", response_model=CreatShortLinkResponse)
@limiter.limit("10/minute")
async def shorten_link(
    create_short_link: CreatShortLinkRequest,
    request: Request,
    service: ShortenLinkService = Depends(get_shorten_link_service),
):
    short_code = request.app.state.id_generator.generate()
    short_link = await service.shorten_link(short_code, create_short_link.long_link)
    short_link = str(request.url) + short_link

    return {"short_link": short_link}


@shorten_link_router.get("/{short_link}")
@limiter.limit("120/minute")
async def redirect_link(
    short_link: str,
    request: Request,
    service: ShortenLinkService = Depends(get_shorten_link_service),
):
    long_link = await service.redirect_link(short_link)

    return RedirectResponse(
        url=long_link,
        status_code=status.HTTP_301_MOVED_PERMANENTLY,
    )
