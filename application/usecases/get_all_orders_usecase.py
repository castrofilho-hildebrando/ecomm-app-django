from typing import TypedDict, List
from datetime import datetime
from application.ports.order_repository import OrderRepository
from domain.errors.access_denied_error import AccessDeniedError


class ActorData(TypedDict):
    id: str
    role: str


class GetAllOrdersInput(TypedDict):
    actor: ActorData


class OrderSummary(TypedDict):
    id: str
    user_id: str
    status: str
    total: float
    created_at: datetime


class GetAllOrdersUseCase:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository
    
    async def execute(self, input_data: GetAllOrdersInput) -> List[OrderSummary]:
        if input_data['actor']['role'] != 'admin':
            raise AccessDeniedError("ACCESS_DENIED", "Access denied")
        
        return await self.order_repository.find_all()