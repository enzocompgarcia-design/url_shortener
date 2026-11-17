class AppException(Exception):
    status_code = 500
    error_code = "app_error"

    def __init__(self, detail: str, *, error_code: str | None = None, status_code: int | None = None):
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