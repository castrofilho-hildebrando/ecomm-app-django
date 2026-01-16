from abc import ABC, abstractmethod
from typing import Optional, List, TypedDict

class CartItem(TypedDict):

    product_id: str
    quantity: int

class CartData(TypedDict):

    user_id: str
    items: List[CartItem]

class CartRepository(ABC):

    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> Optional[CartData]:
        pass
    
    @abstractmethod
    async def add_item(self, user_id: str, product_id: str, quantity: int) -> None:
        pass
    
    @abstractmethod
    async def remove_item(self, user_id: str, product_id: str) -> None:
        pass
    
    @abstractmethod
    async def clear(self, user_id: str) -> None:
        pass