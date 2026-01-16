from domain.errors.invalid_status_transaction_error import InvalidStatusTransactionError
from domain.errors.only_admin_can_change_order_status_error import OnlyAdminCanChangeOrderStatusError


ALLOWED_TRANSITIONS = {
    "pending": ["paid"],
    "paid": ["shipped"],
    "shipped": ["delivered"],
}


class OrderStatusDomainService:
    def validate_transition(self, current_status: str, new_status: str):
        allowed = ALLOWED_TRANSITIONS.get(current_status, [])
        
        if new_status not in allowed:
            raise InvalidStatusTransactionError(
                "INVALID_STATUS_TRANSACTION",
                f"Invalid status transition from {current_status} to {new_status}"
            )
    
    def validate_permission(self, actor_role: str):
        if actor_role != "admin":
            raise OnlyAdminCanChangeOrderStatusError(
                "ONLY_ADMIN_CAN_CHANGE_ORDER_STATUS",
                "Only admin can change order status"
            )