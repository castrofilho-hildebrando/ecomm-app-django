from abc import ABC, abstractmethod
from typing import Optional, List, TypedDict


class ProductData(TypedDict):
    id: str
    price: float
    stock: int


class ProductStockData(TypedDict):
    id: str
    stock: int


class ProductRepository(ABC):
    @abstractmethod
    async def find_by_id(self, product_id: str) -> Optional[ProductStockData]:
        pass
    
    @abstractmethod
    async def find_by_ids(self, product_ids: List[str]) -> List[ProductData]:
        pass
    
    @abstractmethod
    async def decrement_stock(self, product_id: str, quantity: int) -> None:
        pass