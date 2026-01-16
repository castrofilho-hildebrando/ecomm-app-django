from typing import Optional, List
from asgiref.sync import sync_to_async
from application.ports.cart_repository import CartRepository, CartData, CartItem
from apps.cart.models import Cart as CartModel


class DjangoCartRepository(CartRepository):
    @sync_to_async
    def find_by_user_id(self, user_id: str) -> Optional[CartData]:
        try:
            cart = CartModel.objects.get(user_id=user_id)
            return {
                'user_id': str(cart.user_id),
                'items': [
                    {'product_id': str(item.product_id), 'quantity': item.quantity}
                    for item in cart.items.all()
                ]
            }
        except CartModel.DoesNotExist:
            return None
    
    @sync_to_async
    def add_item(self, user_id: str, product_id: str, quantity: int) -> None:
        from apps.cart.models import CartItem as CartItemModel
        
        cart, _ = CartModel.objects.get_or_create(user_id=user_id)
        
        try:
            item = cart.items.get(product_id=product_id)
            item.quantity += quantity
            item.save()
        except CartItemModel.DoesNotExist:
            CartItemModel.objects.create(
                cart=cart,
                product_id=product_id,
                quantity=quantity
            )
    
    @sync_to_async
    def remove_item(self, user_id: str, product_id: str) -> None:
        try:
            cart = CartModel.objects.get(user_id=user_id)
            cart.items.filter(product_id=product_id).delete()
        except CartModel.DoesNotExist:
            pass
    
    @sync_to_async
    def clear(self, user_id: str) -> None:
        try:
            cart = CartModel.objects.get(user_id=user_id)
            cart.items.all().delete()
        except CartModel.DoesNotExist:
            pass