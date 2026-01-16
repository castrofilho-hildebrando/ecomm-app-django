import pytest
from tests.factories import UserFactory, ProductFactory, OrderFactory
from apps.cart.models import Cart


@pytest.mark.django_db
class TestAdminRoutes:
    def test_get_stats_as_admin(self, api_client):
        admin_data = UserFactory.create_with_token(role='admin')
        UserFactory.create_with_token(role='user')
        
        ProductFactory.create(price=100)
        ProductFactory.create(price=50)
        
        response = api_client.get(
            '/api/admin/stats/',
            HTTP_AUTHORIZATION=f"Bearer {admin_data['token']}"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert 'users' in data
        assert 'products' in data
        assert 'orders' in data
        assert 'carts' in data
    
    def test_cannot_get_stats_as_regular_user(self, api_client):
        user_data = UserFactory.create_with_token(role='user')
        
        response = api_client.get(
            '/api/admin/stats/',
            HTTP_AUTHORIZATION=f"Bearer {user_data['token']}"
        )
        
        assert response.status_code == 403
