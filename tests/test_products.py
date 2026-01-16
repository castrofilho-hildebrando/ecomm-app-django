import pytest
import json
from tests.factories import UserFactory, ProductFactory


@pytest.mark.django_db
class TestProductRoutes:
    def test_list_all_products_public(self, api_client):
        ProductFactory.create()
        
        response = api_client.get('/api/products/')
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
    
    def test_create_product_as_admin(self, api_client):
        admin_data = UserFactory.create_with_token(role='admin')
        response = api_client.post(
        '/api/products/create/',
        data=json.dumps({
            'name': 'Laptop Gamer',
            'description': 'Máquina poderosa para jogos.',
            'price': 5000.00,
            'stock': 5
        }),
        content_type='application/json',
        HTTP_AUTHORIZATION=f"Bearer {admin_data['token']}"
    )

    assert response.status_code == 201
    data = response.json()
    assert data['product']['name'] == 'Laptop Gamer'

def test_cannot_create_product_as_regular_user(self, api_client):
    user_data = UserFactory.create_with_token(role='user')

    response = api_client.post(
        '/api/products/create/',
        data=json.dumps({
            'name': 'Laptop Gamer',
            'price': 5000.00
        }),
        content_type='application/json',
        HTTP_AUTHORIZATION=f"Bearer {user_data['token']}"
    )

    assert response.status_code == 403

def test_update_product_as_admin(self, api_client):
    admin_data = UserFactory.create_with_token(role='admin')
    product = ProductFactory.create()

    response = api_client.put(
        f'/api/products/{product.id}/update/',
        data=json.dumps({'price': 299.99}),
        content_type='application/json',
        HTTP_AUTHORIZATION=f"Bearer {admin_data['token']}"
    )

    assert response.status_code == 200
    assert response.json()['product']['price'] == 299.99

def test_delete_product_as_admin(self, api_client):
    admin_data = UserFactory.create_with_token(role='admin')
    product = ProductFactory.create()

    response = api_client.delete(
        f'/api/products/{product.id}/delete/',
        HTTP_AUTHORIZATION=f"Bearer {admin_data['token']}"
    )

    assert response.status_code == 200