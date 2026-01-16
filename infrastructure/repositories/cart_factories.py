from application.usecases.get_cart_usecase import GetCartUseCase
from application.usecases.add_item_to_cart_usecase import AddItemToCartUseCase
from application.usecases.remove_item_from_cart_usecase import RemoveItemFromCartUseCase
from application.usecases.clear_cart_usecase import ClearCartUseCase
from infrastructure.repositories.django_cart_repository import DjangoCartRepository
from infrastructure.repositories.django_product_repository import DjangoProductRepository


def make_get_cart_usecase() -> GetCartUseCase:
    return GetCartUseCase(DjangoCartRepository())


def make_add_item_to_cart_usecase() -> AddItemToCartUseCase:
    return AddItemToCartUseCase(
        DjangoCartRepository(),
        DjangoProductRepository()
    )


def make_remove_item_from_cart_usecase() -> RemoveItemFromCartUseCase:
    return RemoveItemFromCartUseCase(DjangoCartRepository())


def make_clear_cart_usecase() -> ClearCartUseCase:
    return ClearCartUseCase(DjangoCartRepository())