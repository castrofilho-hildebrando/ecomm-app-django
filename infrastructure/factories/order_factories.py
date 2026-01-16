from application.usecases.checkout_usecase import CheckoutUseCase
from application.usecases.list_my_orders_usecase import ListMyOrdersUseCase
from application.usecases.get_all_orders_usecase import GetAllOrdersUseCase
from application.usecases.update_order_status_usecase import UpdateOrderStatusUseCase
from infrastructure.repositories.django_cart_repository import DjangoCartRepository
from infrastructure.repositories.django_product_repository import DjangoProductRepository
from infrastructure.repositories.django_order_repository import DjangoOrderRepository
from infrastructure.repositories.django_outbox_repository import DjangoOutboxRepository
from infrastructure.transaction.django_transaction_manager import DjangoTransactionManager
from infrastructure.factories.cart_factories import make_clear_cart_usecase


def make_checkout_usecase() -> CheckoutUseCase:
    return CheckoutUseCase(
        DjangoCartRepository(),
        DjangoProductRepository(),
        DjangoOrderRepository(),
        DjangoTransactionManager(),
        make_clear_cart_usecase(),
        DjangoOutboxRepository()
    )


def make_list_my_orders_usecase() -> ListMyOrdersUseCase:
    return ListMyOrdersUseCase(DjangoOrderRepository())


def make_get_all_orders_usecase() -> GetAllOrdersUseCase:
    return GetAllOrdersUseCase(DjangoOrderRepository())


def make_update_order_status_usecase() -> UpdateOrderStatusUseCase:
    return UpdateOrderStatusUseCase(DjangoOrderRepository())