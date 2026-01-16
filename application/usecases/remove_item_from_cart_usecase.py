from typing import TypedDict
from application.ports.cart_repository import CartRepository
from domain.errors.cart_not_found_error import CartNotFoundError


class RemoveItemFromCartInput(TypedDict):
    user_id: str
    product_id: str


class RemoveItemFromCartUseCase:
    def __init__(self, cart_repository: CartRepository):
        self.cart_repository = cart_repository
    
    async def execute(self, input_data: RemoveItemFromCartInput) -> None:
        cart = await self.cart_repository.find_by_user_id(input_data['user_id'])
        
        if not cart:
            raise CartNotFoundError(f"Cart for user {input_data['user_id']} not found")
        
        await self.cart_repository.remove_item(
            input_data['user_id'],
            input_data['product_id']
        )