from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from app.errors.exceptions import (
    AppException,
    InvalidLongLink,
    LongLinkNotFound,
)

EXCEPTION_STATUS_MAP = {
    LongLinkNotFound: 404,
    InvalidLongLink: 400,
    RateLimitExceeded: 429,
}


async def app_exception_handler(
    request: Request,
    exc: Exception,
):

    status_code = EXCEPTION_STATUS_MAP.get(type(exc), 500)

    detail = getattr(exc, "detail", str(exc))

    return JSONResponse(
        status_code=status_code,
        content={"detail": str(detail)},
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(
        AppException,
        app_exception_handler,
    )

    app.add_exception_handler(
        RateLimitExceeded,
        app_exception_handler,
    )
