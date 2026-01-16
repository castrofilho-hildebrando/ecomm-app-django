from .domain_error import DomainError


class OnlyAdminCanChangeOrderStatusError(DomainError):
    def __init__(self, code: str = "ONLY_ADMIN_CAN_CHANGE_ORDER_STATUS",
                 message: str = "Only admin can change order status"):
        super().__init__(code, message)