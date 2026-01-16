from typing import List
from domain.errors.order_errors import (
    OrderWithoutItemsError,
    InvalidOrderTotalError,
    OrderCannotBeCancelledError
)
from domain.errors.invalid_status_transaction_error import InvalidStatusTransactionError


class OrderItem:
    def __init__(self, product_id: str, quantity: int):
        self.product_id = product_id
        self.quantity = quantity

class Order:
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    
    STATUS_CHOICES = [PENDING, PAID, SHIPPED, COMPLETED, CANCELLED]
    
    def __init__(self, status: str, items: List[OrderItem], total: float):
        if len(items) == 0:
            raise OrderWithoutItemsError("ORDER_WITHOUT_ITEMS")
        
        if total <= 0:
            raise InvalidOrderTotalError("INVALID_ORDER_TOTAL")
        
        self._status = status
        self._items = items
        self._total = total
    
    @property
    def status(self) -> str:
        return self._status
    
    @property
    def total(self) -> float:
        return self._total
    
    @property
    def items(self) -> List[OrderItem]:
        return self._items.copy()
    
    def mark_as_paid(self):
        if self._status != self.PENDING:
            raise InvalidStatusTransactionError(
                "INVALID_STATUS_TRANSITION",
                f"Cannot pay order in status {self._status}"
            )
        self._status = self.PAID
    
    def ship(self):
        if self._status != self.PAID:
            raise InvalidStatusTransactionError(
                "INVALID_STATUS_TRANSITION",
                f"Cannot ship order in status {self._status}"
            )
        self._status = self.SHIPPED
    
    def complete(self):
        if self._status != self.SHIPPED:
            raise InvalidStatusTransactionError(
                "INVALID_STATUS_TRANSITION",
                f"Cannot complete order in status {self._status}"
            )
        self._status = self.COMPLETED
    
    def cancel(self):
        if self._status == self.SHIPPED:
            raise OrderCannotBeCancelledError(
                "ORDER_CANNOT_BE_CANCELLED",
                "Order already shipped"
            )
        self._status = self.CANCELLED