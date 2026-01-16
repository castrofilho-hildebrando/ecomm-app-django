import pytest
import json
from tests.factories import UserFactory


@pytest.mark.django_db
class TestAuthRoutes:
    def test_register_new_user(self, api_client):
        response = api_client.post(
            '/api/auth/register/',
            data=json.dumps({
                'name': 'Novo Usuário',
                'email': 'novo@example.com',
                'password': '123456'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = response.json()
        assert 'token' in data
        assert data['user']['email'] == 'novo@example.com'
    
    def test_cannot_register_duplicate_email(self, api_client):
        user_data = UserFactory.create_with_token()
        user = user_data['user']
        
        response = api_client.post(
            '/api/auth/register/',
            data=json.dumps({
                'name': 'Hildebrando',
                'email': user.email,
                'password': '123456'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 409
    
    def test_login_with_valid_credentials(self, api_client):
        user_data = UserFactory.create_with_token()
        user = user_data['user']
        
        response = api_client.post(
            '/api/auth/login/',
            data=json.dumps({
                'email': user.email,
                'password': '123456'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.json()
        assert 'token' in data
    
    def test_cannot_login_with_wrong_password(self, api_client):
        user_data = UserFactory.create_with_token()
        user = user_data['user']
        
        response = api_client.post(
            '/api/auth/login/',
            data=json.dumps({
                'email': user.email,
                'password': 'senha_errada'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 401
    
    def test_cannot_login_with_nonexistent_email(self, api_client):
        response = api_client.post(
            '/api/auth/login/',
            data=json.dumps({
                'email': 'naoexiste@example.com',
                'password': '123456'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 401