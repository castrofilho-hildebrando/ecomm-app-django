import json
import asyncio
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from infrastructure.middleware.auth_middleware import authenticate
from infrastructure.factories.cart_factories import (
    make_get_cart_usecase,
    make_add_item_to_cart_usecase,
    make_remove_item_from_cart_usecase,
    make_clear_cart_usecase
)
from domain.errors.domain_error import DomainError


@require_http_methods(["GET"])
@authenticate
def get_cart(request):
    try:
        user_id = request.user_data['user_id']
        
        usecase = make_get_cart_usecase()
        cart = asyncio.run(usecase.execute({'user_id': user_id}))
        
        return JsonResponse({'items': cart['items']})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
@authenticate
def add_item_to_cart(request):
    try:
        user_id = request.user_data['user_id']
        data = json.loads(request.body)
        
        product_id = data.get('productId')
        quantity = data.get('quantity')
        
        if not product_id or not quantity:
            return JsonResponse(
                {'error': 'Produto e quantidade são obrigatórios'},
                status=400
            )
        
        usecase = make_add_item_to_cart_usecase()
        asyncio.run(usecase.execute({
            'user_id': user_id,
            'product_id': product_id,
            'quantity': quantity
        }))
        
        get_usecase = make_get_cart_usecase()
        updated_cart = asyncio.run(get_usecase.execute({'user_id': user_id}))
        
        return JsonResponse({'cart': updated_cart})
    except DomainError as e:
        status = 404 if e.code == "PRODUCT_NOT_FOUND" else 400
        return JsonResponse({'error': e.message}, status=status)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
@authenticate
def remove_item_from_cart(request):
    try:
        user_id = request.user_data['user_id']
        data = json.loads(request.body)
        
        product_id = data.get('productId')
        
        if not product_id:
            return JsonResponse({'error': 'Não autorizado'}, status=401)
        
        # Checar existência do carrinho antes
        get_usecase = make_get_cart_usecase()
        existing = asyncio.run(get_usecase.execute({'user_id': user_id}))
        
        if not existing or len(existing['items']) == 0:
            return JsonResponse({'error': 'Carrinho não existe'}, status=404)
        
        usecase = make_remove_item_from_cart_usecase()
        asyncio.run(usecase.execute({
            'user_id': user_id,
            'product_id': product_id
        }))
        
        updated_cart = asyncio.run(get_usecase.execute({'user_id': user_id}))
        
        return JsonResponse({'cart': updated_cart})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
@authenticate
def clear_cart(request):
    try:
        user_id = request.user_data['user_id']
        
        get_usecase = make_get_cart_usecase()
        existing = asyncio.run(get_usecase.execute({'user_id': user_id}))
        
        if not existing or len(existing['items']) == 0:
            return JsonResponse({'error': 'Carrinho não existe'}, status=404)
        
        usecase = make_clear_cart_usecase()
        asyncio.run(usecase.execute({'user_id': user_id}))
        
        return JsonResponse({
            'message': 'Carrinho limpo com sucesso',
            'cart': {'items': []}
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)