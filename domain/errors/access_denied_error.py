from .domain_error import DomainError


class AccessDeniedError(DomainError):
    def __init__(self, code: str = "ACCESS_DENIED", message: str = "Access denied"):
        super().__init__(code, message)