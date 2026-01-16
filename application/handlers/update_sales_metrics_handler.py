from domain.events.domain_event_handler import DomainEventHandler
from domain.events.order_created_event import OrderCreatedEvent


class UpdateSalesMetricsHandler(DomainEventHandler[OrderCreatedEvent]):
    async def handle(self, event: OrderCreatedEvent) -> None:
        print(f"[METRICS] Nova venda registrada: R$ {event.total}")