from typing import TypedDict
from application.ports.cart_repository import CartRepository


class ClearCartInput(TypedDict):
    user_id: str


class ClearCartUseCase:
    def __init__(self, cart_repository: CartRepository):
        self.cart_repository = cart_repository
    
    async def execute(self, input_data: ClearCartInput) -> None:
        cart = await self.cart_repository.find_by_user_id(input_data['user_id'])
        
        # Comportamento idempotente: se o carrinho não existe, não é erro
        if not cart:
            return
        
        await self.cart_repository.clear(input_data['user_id'])