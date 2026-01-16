import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from infrastructure.middleware.auth_middleware import authenticate, is_admin
from .models import Product


@require_http_methods(["GET"])
def get_all_products(request):
    try:
        products = Product.objects.all()
        products_data = [{
            '_id': str(p.id),
            'id': str(p.id),
            'name': p.name,
            'price': float(p.price),
            'stock': p.stock,
            'description': p.description
        } for p in products]
        
        return JsonResponse(products_data, safe=False)
    except Exception as e:
        print(f"GET PRODUCTS ERROR: {e}")
        return JsonResponse({'error': 'Erro interno'}, status=500)


@require_http_methods(["POST"])
@authenticate
@is_admin
def create_product(request):
    try:
        data = json.loads(request.body)
        
        name = data.get('name')
        price = data.get('price')
        stock = data.get('stock', 0)
        description = data.get('description', '')
        
        if not name or price is None:
            return JsonResponse(
                {'error': 'Campos obrigatórios: name e price'},
                status=400
            )
        
        product = Product.objects.create(
            name=name,
            price=price,
            stock=stock,
            description=description
        )
        
        return JsonResponse({
            'product': {
                '_id': str(product.id),
                'name': product.name,
                'price': float(product.price),
                'stock': product.stock,
                'description': product.description
            }
        }, status=201)
        
    except Exception as e:
        print(f"CREATE PRODUCT ERROR: {e}")
        return JsonResponse({'error': 'Erro interno'}, status=500)


@require_http_methods(["PUT"])
@authenticate
@is_admin
def update_product(request, product_id):
    try:
        data = json.loads(request.body)
        
        product = Product.objects.filter(id=product_id).first()
        
        if not product:
            return JsonResponse({'message': 'Produto não encontrado'}, status=404)
        
        if 'name' in data:
            product.name = data['name']
        if 'price' in data:
            product.price = data['price']
        if 'stock' in data:
            product.stock = data['stock']
        if 'description' in data:
            product.description = data['description']
        
        product.save()
        
        return JsonResponse({
            'product': {
                '_id': str(product.id),
                'name': product.name,
                'price': float(product.price),
                'stock': product.stock,
                'description': product.description
            }
        })
        
    except Exception as e:
        print(f"UPDATE PRODUCT ERROR: {e}")
        return JsonResponse({'error': 'Erro interno'}, status=500)


@require_http_methods(["DELETE"])
@authenticate
@is_admin
def delete_product(request, product_id):
    try:
        product = Product.objects.filter(id=product_id).first()
        
        if not product:
            return JsonResponse({'message': 'Produto não encontrado'}, status=404)
        
        product.delete()
        
        return JsonResponse({
            'product': {
                'deleted': True,
                '_id': str(product_id)
            }
        })
        
    except Exception as e:
        print(f"DELETE PRODUCT ERROR: {e}")
        return JsonResponse({'error': 'Erro interno'}, status=500)