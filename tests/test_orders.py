import pytest
import json
from tests.factories import UserFactory, ProductFactory, CartFactory, CartItemFactory
from apps.orders.models import Order


@pytest.mark.django_db
class TestOrderRoutes:
    def test_checkout_creates_order(self, api_client):
        user_data = UserFactory.create_with_token(role='user')
        product = ProductFactory.create(price=100, stock=10)
        
        cart = CartFactory.create(user_id=user_data['user'].id)
        CartItemFactory.create(cart=cart, product_id=product.id, quantity=2)
        
        response = api_client.post(
            '/api/orders/checkout/',
            HTTP_AUTHORIZATION=f"Bearer {user_data['token']}"
        )
        
        assert response.status_code == 201
        data = response.json()
        assert 'order' in data
        assert data['order']['total'] == 200
    
    def test_cannot_checkout_empty_cart(self, api_client):
        user_data = UserFactory.create_with_token(role='user')
        CartFactory.create(user_id=user_data['user'].id)
        
        response = api_client.post(
            '/api/orders/checkout/',
            HTTP_AUTHORIZATION=f"Bearer {user_data['token']}"
        )
        
        assert response.status_code == 400
        assert 'Carrinho vazio' in response.json()['error']
    
    def test_get_my_orders(self, api_client):
        user_data = UserFactory.create_with_token(role='user')
        from apps.orders.models import Order
        
        Order.objects.create(
            user_id=user_data['user'].id,
            total=100,
            status='pending'
        )
        
        response = api_client.get(
            '/api/orders/my/',
            HTTP_AUTHORIZATION=f"Bearer {user_data['token']}"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
    
    def test_admin_can_get_all_orders(self, api_client):
        admin_data = UserFactory.create_with_token(role='admin')
        user_data = UserFactory.create_with_token(role='user')
        
        Order.objects.create(user_id=user_data['user'].id, total=100, status='pending')
        Order.objects.create(user_id=admin_data['user'].id, total=200, status='pending')
        
        response = api_client.get(
            '/api/orders/all/',
            HTTP_AUTHORIZATION=f"Bearer {admin_data['token']}"
        )
        
        assert response.status_code == 200
        assert len(response.json()) == 2
    
    def test_regular_user_cannot_get_all_orders(self, api_client):
        user_data = UserFactory.create_with_token(role='user')
        
        response = api_client.get(
            '/api/orders/all/',
            HTTP_AUTHORIZATION=f"Bearer {user_data['token']}"
        )
        
        assert response.status_code == 403