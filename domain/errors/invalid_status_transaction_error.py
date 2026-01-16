from .domain_error import DomainError


class InvalidStatusTransactionError(DomainError):
    def __init__(self, code: str = "INVALID_STATUS_TRANSACTION", message: str = "Invalid status transaction"):
        super().__init__(code, message)