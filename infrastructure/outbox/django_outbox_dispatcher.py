from typing import Dict
from asgiref.sync import sync_to_async
from infrastructure.outbox.outbox_dispatcher import OutboxDispatcher
from infrastructure.outbox.handlers.order_placed_handler import OrderPlacedHandler
from apps.orders.models import Outbox


class DjangoOutboxDispatcher(OutboxDispatcher):
    def __init__(self):
        self.handlers: Dict[str, any] = {
            "order.placed": OrderPlacedHandler(),
        }
    
    async def dispatch(self) -> None:
        events = await self._get_unprocessed_events()
        
        for event in events:
            handler = self.handlers.get(event.name)
            
            if not handler:
                await self._mark_as_processed(event)
                continue
            
            await handler.handle({
                'name': event.name,
                'payload': event.payload,
                'occurred_at': event.occurred_at
            })
            
            await self._mark_as_processed(event)
    
    @sync_to_async
    def _get_unprocessed_events(self):
        return list(Outbox.objects.filter(processed=False))
    
    @sync_to_async
    def _mark_as_processed(self, event):
        from django.utils import timezone
        event.processed = True
        event.processed_at = timezone.now()
        event.save()