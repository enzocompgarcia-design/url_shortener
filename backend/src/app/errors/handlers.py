from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from app.errors.exceptions import AppException


async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_code": exc.error_code,
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        serialized = dict(error)
        ctx = serialized.get("ctx")
        if isinstance(ctx, dict):
            serialized["ctx"] = {
                key: str(value) if isinstance(value, BaseException) else value
                for key, value in ctx.items()
            }
        errors.append(serialized)

    return JSONResponse(
        status_code=422,
        content={
            "detail": errors,
            "error_code": "validation_error",
        },
    )


async def rate_limit_exception_handler(request: Request, exc: RateLimitExceeded):
    detail = getattr(exc, "detail", "Rate limit exceeded")
    return JSONResponse(
        status_code=429,
        content={
            "detail": str(detail),
            "error_code": "rate_limit_exceeded",
        },
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Erro interno do servidor",
            "error_code": "internal_server_error",
        },
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
