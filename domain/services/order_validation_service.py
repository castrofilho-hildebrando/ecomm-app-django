from typing import List
from domain.types.order_item import OrderItem
from domain.types.product_snapshot import ProductSnapshot
from domain.errors.checkout_errors import ProductNotFoundError, InsufficientStockError


class OrderValidationService:
    def validate_and_calculate_total(
        self, 
        items: List[OrderItem], 
        products: List[ProductSnapshot]
    ) -> float:
        product_map = {p['id']: p for p in products}
        total = 0
        
        for item in items:
            product = product_map.get(item['product_id'])
            
            if not product:
                raise ProductNotFoundError(item['product_id'])
            
            if product['stock'] < item['quantity']:
                raise InsufficientStockError(
                    item['product_id'],
                    product['stock'],
                    item['quantity']
                )
            
            total += product['price'] * item['quantity']
        
        return total