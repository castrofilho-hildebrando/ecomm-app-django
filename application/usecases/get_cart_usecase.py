from typing import TypedDict, List
from application.ports.cart_repository import CartRepository


class GetCartInput(TypedDict):
    user_id: str


class CartItemOutput(TypedDict):
    product_id: str
    quantity: int


class CartOutput(TypedDict):
    items: List[CartItemOutput]


class GetCartUseCase:
    def __init__(self, cart_repository: CartRepository):
        self.cart_repository = cart_repository
    
    async def execute(self, input_data: GetCartInput) -> CartOutput:
        cart = await self.cart_repository.find_by_user_id(input_data['user_id'])
        
        return {
            'items': cart['items'] if cart else []
        }