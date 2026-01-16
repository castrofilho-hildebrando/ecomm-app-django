from .domain_error import DomainError


class OrderNotFoundError(DomainError):
    def __init__(self, code: str = "ORDER_NOT_FOUND", message: str = "Order not found"):
        super().__init__(code, message)


class OrderWithoutItemsError(DomainError):
    def __init__(self, code: str = "ORDER_WITHOUT_ITEMS", message: str = "Order without items"):
        super().__init__(code, message)


class InvalidOrderTotalError(DomainError):
    def __init__(self, code: str = "INVALID_ORDER_TOTAL", message: str = "Invalid order total"):
        super().__init__(code, message)


class OrderCannotBeCancelledError(DomainError):
    def __init__(self, code: str = "ORDER_CANNOT_BE_CANCELLED", message: str = "Order cannot be cancelled"):
        super().__init__(code, message)