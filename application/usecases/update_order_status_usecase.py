from typing import TypedDict
from application.ports.order_repository import OrderRepository
from domain.services.order_status_domain_service import OrderStatusDomainService
from domain.errors.order_errors import OrderNotFoundError

class ActorData(TypedDict):

    id: str
    role: str

class UpdateOrderStatusInput(TypedDict):

    order_id: str
    new_status: str
    actor: ActorData

class UpdateOrderStatusOutput(TypedDict):

    order_id: str
    previous_status: str
    current_status: str

class UpdateOrderStatusUseCase:

    def init(self, order_repository: OrderRepository):
        self.order_repository = order_repository
        self.status_service = OrderStatusDomainService()

        async def execute(self, input_data: UpdateOrderStatusInput) -> UpdateOrderStatusOutput:

            order = await self.order_repository.find_by_id(input_data['order_id'])

            if not order:
                raise OrderNotFoundError("ORDER_NOT_FOUND", "Order not found")

            self.status_service.validate_permission(input_data['actor']['role'])
            self.status_service.validate_transition(order['status'], input_data['new_status'])

            await self.order_repository.update_status(
                order['id'],
                input_data['new_status']
            )

            return {
                'order_id': order['id'],
                'previous_status': order['status'],
                'current_status': input_data['new_status']
            }
