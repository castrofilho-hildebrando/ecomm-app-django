from typing import Optional, List
from asgiref.sync import sync_to_async
from application.ports.order_repository import (
    OrderRepository, OrderData, OrderDataWithDate, CreateOrderData
)
from apps.orders.models import Order, OrderItem


class DjangoOrderRepository(OrderRepository):
    @sync_to_async
    def find_by_id(self, order_id: str) -> Optional[OrderData]:
        try:
            order = Order.objects.prefetch_related('items').get(id=order_id)
            return self._order_to_dict(order)
        except Order.DoesNotExist:
            return None
    
    @sync_to_async
    def find_by_user_id(self, user_id: str) -> List[OrderData]:
        orders = Order.objects.filter(user_id=user_id).prefetch_related('items')
        return [self._order_to_dict(order) for order in orders]
    
    @sync_to_async
    def find_all(self) -> List[OrderDataWithDate]:
        orders = Order.objects.all().prefetch_related('items')
        return [self._order_to_dict_with_date(order) for order in orders]
    
    @sync_to_async
    def create(self, data: CreateOrderData) -> OrderData:
        order = Order.objects.create(
            user_id=data['user_id'],
            total=data['total'],
            status=data['status']
        )
        
        for item in data['items']:
            OrderItem.objects.create(
                order=order,
                product_id=item['product_id'],
                quantity=item['quantity']
            )
        
        order.refresh_from_db()
        return self._order_to_dict(order)
    
    @sync_to_async
    def update_status(self, order_id: str, status: str) -> Optional[OrderData]:
        try:
            order = Order.objects.get(id=order_id)
            order.status = status
            order.save()
            return self._order_to_dict(order)
        except Order.DoesNotExist:
            return None
    
    def _order_to_dict(self, order: Order) -> OrderData:
        return {
            'id': str(order.id),
            'user_id': str(order.user_id),
            'items': [
                {'product_id': str(item.product_id), 'quantity': item.quantity}
                for item in order.items.all()
            ],
            'total': float(order.total),
            'status': order.status
        }
    
    def _order_to_dict_with_date(self, order: Order) -> OrderDataWithDate:
        base = self._order_to_dict(order)
        base['created_at'] = order.created_at
        return base
