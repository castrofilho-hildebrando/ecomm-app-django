from typing import TypedDict


class OrderItem(TypedDict):
    product_id: str
    quantity: int