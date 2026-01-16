from typing import TypedDict


class ProductSnapshot(TypedDict):
    id: str
    price: float
    stock: int