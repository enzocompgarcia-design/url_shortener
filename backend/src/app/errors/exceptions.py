from app.config import config


class AppException(Exception):
    status_code = 500
    error_code = "app_error"

    def __init__(
        self,
        detail: str,
        *,
        error_code: str | None = None,
        status_code: int | None = None,
    ):
        self.detail = detail
        if error_code is not None:
            self.error_code = error_code
        if status_code is not None:
            self.status_code = status_code
        super().__init__(detail)


class LongLinkNotFound(AppException):
    status_code = 404
    error_code = "long_link_not_found"

    def __init__(self, short_link: str | None = None):
        detail = "Link não encontrado"
        if short_link:
            detail = f"Link curto '{short_link}' não encontrado"
        super().__init__(detail)


class InvalidLongLink(AppException):
    status_code = 400
    error_code = "invalid_long_link"

    def __init__(self, link: str):
        super().__init__(f"Link inválido: '{link}'")


class InvalidProtocol(AppException):
    status_code = 406
    error_code = "invalid_protocol"

    def __init__(self, protocolo: str):
        super().__init__(
            f"Protocolo inválido: {protocolo}, protocolos válidos: {config.ALLOWED_PROTOCOLS}"
        )


class CacheUnavailable(AppException):
    status_code = 503
    error_code = "cache_unavailable"

    def __init__(self, detail: str = "Cache indisponível"):
        super().__init__(detail)


class DatabaseUnavailable(AppException):
    status_code = 503
    error_code = "database_unavailable"

    def __init__(self, detail: str = "Banco de dados indisponível"):
        super().__init__(detail)
