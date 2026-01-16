import factory
import bcrypt
import jwt
from django.conf import settings
from apps.users.models import User
from apps.products.models import Product
from apps.cart.models import Cart, CartItem
from apps.orders.models import Order, OrderItem
from apps.addresses.models import Address


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    name = "Hildebrando"
    email = factory.Sequence(lambda n: f"user-{n}@example.com")
    role = "user"
    
    @factory.lazy_attribute
    def password(self):
        return bcrypt.hashpw(b"123456", bcrypt.gensalt()).decode('utf-8')
    
    @classmethod
    def create_with_token(cls, role='user', suffix=None):
        if suffix is None:
            import time
            suffix = str(int(time.time() * 1000))
        
        email = f"{'admin' if role == 'admin' else 'user'}-{suffix}@example.com"
        
        user = cls.create(
            email=email,
            role=role
        )
        
        token = jwt.encode(
            {'user_id': str(user.id), 'role': user.role},
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )
        
        return {'user': user, 'token': token}


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
    
    name = "Produto Teste"
    description = "Descrição do produto teste"
    price = 99.99
    stock = 10


class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart


class CartItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CartItem
    
    quantity = 1


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order
    
    total = 100.00
    status = "pending"


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem
    
    quantity = 1


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address
    
    street = "Rua Teste, 123"
    city = "Cidade Teste"
    state = "SP"
    zip_code = "12345-678"
    country = "Brasil"
    is_default = False