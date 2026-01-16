from typing import TypedDict, List
from datetime import datetime
from typing import Optional
from application.ports.order_repository import OrderRepository


class ListMyOrdersInput(TypedDict):
    user_id: str


class OrderSummary(TypedDict):
    id: str
    status: str
    total: float
    created_at: Optional[datetime]


class ListMyOrdersUseCase:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository
    
    async def execute(self, input_data: ListMyOrdersInput) -> List[OrderSummary]:
        return await self.order_repository.find_by_user_id(input_data['user_id'])