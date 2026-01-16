import json
import asyncio
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from infrastructure.middleware.auth_middleware import authenticate, is_admin
from infrastructure.factories.order_factories import (
    make_checkout_usecase,
    make_list_my_orders_usecase,
    make_get_all_orders_usecase,
    make_update_order_status_usecase
)
from infrastructure.repositories.django_order_repository import DjangoOrderRepository
from domain.errors.domain_error import DomainError


@require_http_methods(["POST"])
@authenticate
def checkout(request):
    try:
        user_id = request.user_data['user_id']
        
        checkout_usecase = make_checkout_usecase()
        result = asyncio.run(checkout_usecase.execute({'user_id': user_id}))
        
        return JsonResponse({
            'order': {
                '_id': result['order_id'],
                'status': result['status'],
                'total': result['total']
            }
        }, status=201)
    except DomainError as e:
        known = ["CART_EMPTY", "PRODUCT_NOT_FOUND", "INSUFFICIENT_STOCK"]
        status = 400 if e.code in known else 500
        return JsonResponse({'error': e.message}, status=status)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Alias for checkout
create_order = checkout


@require_http_methods(["PUT"])
@authenticate
@is_admin
def update_order_status(request, order_id):
    try:
        data = json.loads(request.body)
        status = data.get('status')
        
        repository = DjangoOrderRepository()
        updated_order = asyncio.run(repository.update_status(str(order_id), status))
        
        if not updated_order:
            return JsonResponse({'message': 'Order not found'}, status=404)
        
        return JsonResponse({
            '_id': updated_order['id'],
            'status': updated_order['status'],
            'total': updated_order['total']
        })
    except Exception:
        return JsonResponse({'error': 'Erro interno'}, status=500)


@require_http_methods(["GET"])
@authenticate
def get_my_orders(request):
    try:
        user_id = request.user_data['user_id']
        
        repository = DjangoOrderRepository()
        orders = asyncio.run(repository.find_by_user_id(user_id))
        
        orders_with_id = [
            {**order, '_id': order['id']}
            for order in orders
        ]
        
        return JsonResponse(orders_with_id, safe=False)
    except Exception:
        return JsonResponse({'error': 'Erro interno'}, status=500)


@require_http_methods(["GET"])
@authenticate
def get_all_orders(request):
    try:
        user_data = request.user_data
        
        if user_data['role'] != 'admin':
            return JsonResponse({'message': 'Forbidden'}, status=403)
        
        usecase = make_get_all_orders_usecase()
        orders = asyncio.run(usecase.execute({
            'actor': {
                'id': user_data['user_id'],
                'role': user_data['role']
            }
        }))
        
        return JsonResponse(orders, safe=False)
    except DomainError as e:
        return JsonResponse({'message': e.message}, status=403)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)