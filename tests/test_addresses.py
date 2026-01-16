import pytest
import json
from tests.factories import UserFactory, AddressFactory


@pytest.mark.django_db
class TestAddressRoutes:
    def test_create_address(self, api_client):
        user_data = UserFactory.create_with_token(role='user')
        
        response = api_client.post(
            '/api/addresses/create/',
            data=json.dumps({
                'street': 'Rua Teste, 123',
                'city': 'Cidade Teste',
                'state': 'SP',
                'zipCode': '12345-678',
                'country': 'Brasil'
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {user_data['token']}"
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data['address']['street'] == 'Rua Teste, 123'
    
    def test_get_user_addresses(self, api_client):
        user_data = UserFactory.create_with_token(role='user')
        AddressFactory.create(user_id=user_data['user'].id)
        
        response = api_client.get(
            '/api/addresses/',
            HTTP_AUTHORIZATION=f"Bearer {user_data['token']}"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
    
    def test_update_address(self, api_client):
        user_data = UserFactory.create_with_token(role='user')
        address = AddressFactory.create(user_id=user_data['user'].id)
        
        response = api_client.put(
            f'/api/addresses/{address.id}/update/',
            data=json.dumps({'street': 'Nova Rua, 999'}),
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {user_data['token']}"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['address']['street'] == 'Nova Rua, 999'
    
    def test_delete_address(self, api_client):
        user_data = UserFactory.create_with_token(role='user')
        address = AddressFactory.create(user_id=user_data['user'].id)
        
        response = api_client.delete(
            f'/api/addresses/{address.id}/delete/',
            HTTP_AUTHORIZATION=f"Bearer {user_data['token']}"
        )
        
        assert response.status_code == 200
        assert 'removido com sucesso' in response.json()['message']
