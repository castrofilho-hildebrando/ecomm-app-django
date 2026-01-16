from typing import TypedDict
from application.ports.cart_repository import CartRepository
from application.ports.product_repository import ProductRepository
from domain.errors.checkout_errors import ProductNotFoundError, InsufficientStockError


class AddItemToCartInput(TypedDict):
    user_id: str
    product_id: str
    quantity: int


class AddItemToCartUseCase:
    def __init__(
        self,
        cart_repository: CartRepository,
        product_repository: ProductRepository
    ):
        self.cart_repository = cart_repository
        self.product_repository = product_repository
    
    async def execute(self, input_data: AddItemToCartInput) -> None:
        # Verificar se o produto existe
        product = await self.product_repository.find_by_id(input_data['product_id'])
        
        if not product:
            raise ProductNotFoundError(input_data['product_id'])
        
        # Verificar estoque
        if product['stock'] < input_data['quantity']:
            raise InsufficientStockError(
                input_data['product_id'],
                product['stock'],
                input_data['quantity']
            )
        
        # Delegar a persistência ao repositório
        await self.cart_repository.add_item(
            input_data['user_id'],
            input_data['product_id'],
            input_data['quantity']
        )