import pytest
import json
from tests.factories import UserFactory


@pytest.mark.django_db
class TestUserRoutes:
    def test_list_users_as_admin(self, api_client):
        admin_data = UserFactory.create_with_token(role='admin')
        UserFactory.create_with_token(role='user')
        
        response = api_client.get(
            '/api/users/',
            HTTP_AUTHORIZATION=f"Bearer {admin_data['token']}"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2
    
    def test_cannot_list_users_without_admin(self, api_client):
        user_data = UserFactory.create_with_token(role='user')
        
        response = api_client.get(
            '/api/users/',
            HTTP_AUTHORIZATION=f"Bearer {user_data['token']}"
        )
        
        assert response.status_code == 403
    
    def test_get_user_by_id_as_admin(self, api_client):
        admin_data = UserFactory.create_with_token(role='admin')
        user_data = UserFactory.create_with_token(role='user')
        
        response = api_client.get(
            f'/api/users/{user_data["user"].id}/',
            HTTP_AUTHORIZATION=f"Bearer {admin_data['token']}"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert 'email' in data
        assert 'name' in data
    
    def test_update_user_as_admin(self, api_client):
        admin_data = UserFactory.create_with_token(role='admin')
        user_data = UserFactory.create_with_token(role='user')
        
        response = api_client.put(
            f'/api/users/{user_data["user"].id}/update/',
            data=json.dumps({'name': 'Nome Atualizado'}),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {admin_data['token']}"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['user']['name'] == 'Nome Atualizado'
    
    def test_delete_user_as_admin(self, api_client):
        admin_data = UserFactory.create_with_token(role='admin')
        user_data = UserFactory.create_with_token(role='user')
        
        response = api_client.delete(
            f'/api/users/{user_data["user"].id}/delete/',
            HTTP_AUTHORIZATION=f"Bearer {admin_data['token']}"
        )
        
        assert response.status_code == 200
        assert 'removido com sucesso' in response.json()['message']