from domain.events.domain_event_handler import DomainEventHandler
from domain.events.order_created_event import OrderCreatedEvent


class SendOrderEmailHandler(DomainEventHandler[OrderCreatedEvent]):
    async def handle(self, event: OrderCreatedEvent) -> None:
        print(f"[EMAIL] Pedido {event.order_id} criado para usuário {event.user_id}")