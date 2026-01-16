from datetime import datetime


class OrderCreatedEvent:
    def __init__(self, order_id: str, user_id: str, total: float):
        self.order_id = order_id
        self.user_id = user_id
        self.total = total
        self.occurred_at = datetime.now()