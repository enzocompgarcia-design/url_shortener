class AppException(Exception):
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


class LongLinkNotFound(AppException):
    def __init__(self):
        super().__init__("link não encontrado")

class InvalidLongLink(AppException):
    def __init__(self, link: str):
        super().__init__(f"link: '{link}' não é válido")