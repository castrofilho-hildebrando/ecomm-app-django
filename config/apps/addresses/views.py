import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from infrastructure.middleware.auth_middleware import authenticate
from .models import Address


def ensure_only_one_default(user_id, current_address_id=None):
    filter_dict = {'user_id': user_id}
    
    if current_address_id:
        Address.objects.filter(user_id=user_id).exclude(id=current_address_id).update(is_default=False)
    else:
        Address.objects.filter(**filter_dict).update(is_default=False)


@require_http_methods(["POST"])
@authenticate
def create_address(request):
    try:
        user_id = request.user_data['user_id']
        data = json.loads(request.body)
        
        street = data.get('street')
        city = data.get('city')
        state = data.get('state')
        zip_code = data.get('zipCode')
        country = data.get('country', 'Brazil')
        is_default = data.get('isDefault', False)
        
        if not street or not city or not state or not zip_code:
            return JsonResponse(
                {'error': 'Campos obrigatórios ausentes.'},
                status=400
            )
        
        if is_default:
            ensure_only_one_default(user_id)
        
        address = Address.objects.create(
            user_id=user_id,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code,
            country=country,
            is_default=is_default
        )
        
        address_data = {
            '_id': str(address.id),
            'userId': str(address.user_id),
            'street': address.street,
            'city': address.city,
            'state': address.state,
            'zipCode': address.zip_code,
            'country': address.country,
            'isDefault': address.is_default
        }
        
        return JsonResponse({
            'message': 'Endereço criado com sucesso',
            'address': address_data
        }, status=201)
        
    except Exception as e:
        print(f"Erro ao criar endereço: {e}")
        return JsonResponse({'error': 'Erro interno ao criar endereço.'}, status=500)


@require_http_methods(["GET"])
@authenticate
def get_addresses(request):
    try:
        user_id = request.user_data['user_id']
        
        addresses = Address.objects.filter(user_id=user_id).order_by('-is_default', 'created_at')
        
        addresses_data = [{
            '_id': str(addr.id),
            'userId': str(addr.user_id),
            'street': addr.street,
            'city': addr.city,
            'state': addr.state,
            'zipCode': addr.zip_code,
            'country': addr.country,
            'isDefault': addr.is_default
        } for addr in addresses]
        
        return JsonResponse(addresses_data, safe=False)
        
    except Exception as e:
        print(f"Erro ao buscar endereços: {e}")
        return JsonResponse({'error': 'Erro interno ao buscar endereços.'}, status=500)


@require_http_methods(["PUT"])
@authenticate
def update_address(request, address_id):
    try:
        user_id = request.user_data['user_id']
        data = json.loads(request.body)
        
        address = Address.objects.filter(id=address_id, user_id=user_id).first()
        
        if not address:
            return JsonResponse(
                {'error': 'Endereço não encontrado ou não pertence ao usuário.'},
                status=404
            )
        
        if data.get('isDefault') is True:
            ensure_only_one_default(user_id, address_id)
        
        if 'street' in data:
            address.street = data['street']
        if 'city' in data:
            address.city = data['city']
        if 'state' in data:
            address.state = data['state']
        if 'zipCode' in data:
            address.zip_code = data['zipCode']
        if 'country' in data:
            address.country = data['country']
        if 'isDefault' in data:
            address.is_default = data['isDefault']
        
        address.save()
        
        address_data = {
            '_id': str(address.id),
            'userId': str(address.user_id),
            'street': address.street,
            'city': address.city,
            'state': address.state,
            'zipCode': address.zip_code,
            'country': address.country,
            'isDefault': address.is_default
        }
        
        return JsonResponse({
            'message': 'Endereço atualizado com sucesso',
            'address': address_data
        })
        
    except Exception as e:
        print(f"Erro ao atualizar endereço: {e}")
        return JsonResponse({'error': 'Erro interno ao atualizar endereço.'}, status=500)


@require_http_methods(["DELETE"])
@authenticate
def delete_address(request, address_id):
    try:
        user_id = request.user_data['user_id']
        
        address = Address.objects.filter(id=address_id, user_id=user_id).first()
        
        if not address:
            return JsonResponse(
                {'error': 'Endereço não encontrado ou não pertence ao usuário.'},
                status=404
            )
        
        address.delete()
        
        return JsonResponse({'message': 'Endereço removido com sucesso'})
        
    except Exception as e:
        print(f"Erro ao deletar endereço: {e}")
        return JsonResponse({'error': 'Erro interno ao deletar endereço.'}, status=500)