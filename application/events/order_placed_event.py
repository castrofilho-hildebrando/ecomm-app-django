from datetime import datetime
from typing import TypedDict
from application.events.application_event import ApplicationEvent


class OrderPlacedPayload(TypedDict):
    order_id: str
    user_id: str
    total: float


class OrderPlacedEvent(ApplicationEvent):
    def __init__(self, payload: OrderPlacedPayload):
        self.name = "order.placed"
        self.occurred_at = datetime.now()
        self.payload = payload