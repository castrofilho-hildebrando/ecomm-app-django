import pytest
import json
from tests.factories import UserFactory, ProductFactory


@pytest.mark.django_db
class TestCartRoutes:
    def test_get_empty_cart(self, api_client):
        user_data = UserFactory.create_with_token(role='user')
        
        response = api_client.get(
            '/api/cart/',
            HTTP_AUTHORIZATION=f"Bearer {user_data['token']}"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data.get('items', [])) == 0
    
    def test_add_item_to_cart(self, api_client):
        user_data = UserFactory.create_with_token(role='user')
        product = ProductFactory.create()
        
        response = api_client.post(
            '/api/cart/add/',
            data=json.dumps({
                'productId': str(product.id),
                'quantity': 2
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {user_data['token']}"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data['cart']['items']) == 1
        assert data['cart']['items'][0]['quantity'] == 2
    
    def test_cannot_add_nonexistent_product(self, api_client):
        user_data = UserFactory.create_with_token(role='user')
        
        response = api_client.post(
            '/api/cart/add/',
            data=json.dumps({
                'productId': '00000000-0000-0000-0000-000000000000',
                'quantity': 1
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {user_data['token']}"
        )
        
        assert response.status_code == 404
    
    def test_remove_item_from_cart(self, api_client):
        user_data = UserFactory.create_with_token(role='user')
        product = ProductFactory.create()
        
        # Add item first
        api_client.post(
            '/api/cart/add/',
            data=json.dumps({
                'productId': str(product.id),
                'quantity': 2
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {user_data['token']}"
        )
        
        # Remove item
        response = api_client.post(
            '/api/cart/remove/',
            data=json.dumps({'productId': str(product.id)}),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {user_data['token']}"
        )
        
        assert response.status_code == 200
        assert len(response.json()['cart']['items']) == 0
    
    def test_clear_cart(self, api_client):
        user_data = UserFactory.create_with_token(role='user')
        product = ProductFactory.create()
        
        # Add item first
        api_client.post(
            '/api/cart/add/',
            data=json.dumps({
                'productId': str(product.id),
                'quantity': 2
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {user_data['token']}"
        )
        
        # Clear cart
        response = api_client.post(
            '/api/cart/clear/',
            HTTP_AUTHORIZATION=f"Bearer {user_data['token']}"
        )
        
        assert response.status_code == 200
        assert len(response.json()['cart']['items']) == 0
