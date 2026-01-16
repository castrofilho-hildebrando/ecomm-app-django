from abc import ABC, abstractmethod
from typing import Optional, List, TypedDict, Any
from datetime import datetime


class OrderData(TypedDict):
    id: str
    user_id: str
    items: List[Any]
    total: float
    status: str


class OrderDataWithDate(OrderData):
    created_at: datetime


class CreateOrderData(TypedDict):
    user_id: str
    items: List[Any]
    total: float
    status: str


class OrderRepository(ABC):
    @abstractmethod
    async def find_by_id(self, order_id: str) -> Optional[OrderData]:
        pass
    
    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> List[OrderData]:
        pass
    
    @abstractmethod
    async def find_all(self) -> List[OrderDataWithDate]:
        pass
    
    @abstractmethod
    async def create(self, data: CreateOrderData) -> OrderData:
        pass
    
    @abstractmethod
    async def update_status(self, order_id: str, status: str) -> Optional[OrderData]:
        pass