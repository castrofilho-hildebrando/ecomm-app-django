from typing import TypedDict
from application.ports.cart_repository import CartRepository
from application.ports.product_repository import ProductRepository
from application.ports.order_repository import OrderRepository
from application.ports.transaction_manager import TransactionManager
from application.ports.outbox_repository import OutboxRepository
from application.usecases.clear_cart_usecase import ClearCartUseCase
from domain.errors.checkout_errors import CartEmptyError
from domain.services.order_validation_service import OrderValidationService


class CheckoutInput(TypedDict):
    user_id: str


class CheckoutOutput(TypedDict):
    order_id: str
    status: str
    total: float


class CheckoutUseCase:
    def __init__(
        self,
        cart_repository: CartRepository,
        product_repository: ProductRepository,
        order_repository: OrderRepository,
        transaction_manager: TransactionManager,
        clear_cart_usecase: ClearCartUseCase,
        outbox_repository: OutboxRepository
    ):
        self.cart_repository = cart_repository
        self.product_repository = product_repository
        self.order_repository = order_repository
        self.transaction_manager = transaction_manager
        self.clear_cart_usecase = clear_cart_usecase
        self.outbox_repository = outbox_repository
    
    async def execute(self, input_data: CheckoutInput) -> CheckoutOutput:
        async def transaction_logic():
            cart = await self.cart_repository.find_by_user_id(input_data['user_id'])
            
            if not cart or len(cart['items']) == 0:
                raise CartEmptyError()
            
            product_ids = [item['product_id'] for item in cart['items']]
            products = await self.product_repository.find_by_ids(product_ids)
            
            validation_service = OrderValidationService()
            total = validation_service.validate_and_calculate_total(cart['items'], products)
            
            for item in cart['items']:
                await self.product_repository.decrement_stock(
                    item['product_id'],
                    item['quantity']
                )
            
            order = await self.order_repository.create({
                'user_id': input_data['user_id'],
                'items': cart['items'],
                'total': total,
                'status': 'pending'
            })
            
            await self.clear_cart_usecase.execute({'user_id': input_data['user_id']})
            
            # Persistir evento no Outbox
            from application.events.order_placed_event import OrderPlacedEvent
            await self.outbox_repository.save(
                OrderPlacedEvent({
                    'order_id': order['id'],
                    'user_id': input_data['user_id'],
                    'total': total
                })
            )
            
            return {
                'order_id': order['id'],
                'status': 'pending',
                'total': total
            }
        
        return await self.transaction_manager.run_in_transaction(transaction_logic)