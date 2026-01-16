from .domain_error import DomainError


class CartEmptyError(DomainError):
    def __init__(self):
        super().__init__("CART_EMPTY", "Carrinho vazio")


class ProductNotFoundError(DomainError):
    def __init__(self, product_id: str = None):
        message = f"Produto {product_id} não encontrado" if product_id else "Produto não encontrado"
        super().__init__("PRODUCT_NOT_FOUND", message)
        self.product_id = product_id


class InsufficientStockError(DomainError):
    def __init__(self, product_id: str, available: int, requested: int):
        message = f"Estoque insuficiente para o produto {product_id}. Disponível: {available}, solicitado: {requested}"
        super().__init__("INSUFFICIENT_STOCK", message)
        self.product_id = product_id
        self.available = available
        self.requested = requested