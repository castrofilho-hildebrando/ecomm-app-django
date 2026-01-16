from typing import Dict, List, Type
from domain.events.domain_event_handler import DomainEventHandler


class EventBus:
    def __init__(self):
        self._handlers: Dict[str, List[DomainEventHandler]] = {}
    
    def subscribe(self, event_class: Type, handler: DomainEventHandler):
        event_name = event_class.__name__
        
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        
        self._handlers[event_name].append(handler)
    
    async def publish(self, event):
        event_name = event.__class__.__name__
        handlers = self._handlers.get(event_name, [])
        
        for handler in handlers:
            await handler.handle(event)