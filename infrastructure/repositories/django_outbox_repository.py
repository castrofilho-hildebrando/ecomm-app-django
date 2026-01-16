from asgiref.sync import sync_to_async
from application.ports.outbox_repository import OutboxRepository
from application.events.application_event import ApplicationEvent
from apps.orders.models import Outbox


class DjangoOutboxRepository(OutboxRepository):
    @sync_to_async
    def save(self, event: ApplicationEvent) -> None:
        Outbox.objects.create(
            name=event.name,
            payload=event.payload,
            occurred_at=event.occurred_at,
            processed=False
        )