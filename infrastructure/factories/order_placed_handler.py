from application.events.application_event import ApplicationEvent


class OrderPlacedHandler:
    async def handle(self, event: ApplicationEvent) -> None:
        payload = event.payload
        order_id = payload['order_id']
        user_id = payload['user_id']
        total = payload['total']
        
        print(f"[OrderPlacedHandler] {{'orderId': '{order_id}', 'userId': '{user_id}', 'total': {total}}}")