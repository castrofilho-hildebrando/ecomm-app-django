from typing import Optional, List
from asgiref.sync import sync_to_async
from application.ports.product_repository import ProductRepository, ProductData, ProductStockData
from apps.products.models import Product


class DjangoProductRepository(ProductRepository):
    @sync_to_async
    def find_by_id(self, product_id: str) -> Optional[ProductStockData]:
        try:
            product = Product.objects.get(id=product_id)
            return {
                'id': str(product.id),
                'stock': product.stock
            }
        except Product.DoesNotExist:
            return None
    
    @sync_to_async
    def find_by_ids(self, product_ids: List[str]) -> List[ProductData]:
        products = Product.objects.filter(id__in=product_ids)
        return [
            {
                'id': str(p.id),
                'price': float(p.price),
                'stock': p.stock
            }
            for p in products
        ]
    
    @sync_to_async
    def decrement_stock(self, product_id: str, quantity: int) -> None:
        from django.db.models import F
        Product.objects.filter(id=product_id).update(stock=F('stock') - quantity)