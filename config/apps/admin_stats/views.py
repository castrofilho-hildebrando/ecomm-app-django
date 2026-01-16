from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Sum, Count, Q
from infrastructure.middleware.auth_middleware import authenticate, is_admin
from apps.users.models import User
from apps.products.models import Product
from apps.orders.models import Order
from apps.cart.models import Cart
from datetime import datetime


@require_http_methods(["GET"])
@authenticate
@is_admin
def get_stats(request):
    try:
        start_date_str = request.GET.get('startDate')
        end_date_str = request.GET.get('endDate')
        
        start = datetime.fromisoformat(start_date_str) if start_date_str else datetime(1970, 1, 1)
        end = datetime.fromisoformat(end_date_str) if end_date_str else datetime.now()
        
        date_filter = Q(created_at__gte=start, created_at__lte=end)
        
        # Users
        users = User.objects.filter(date_filter)
        total_users = users.count()
        admins = users.filter(role='admin').count()
        normal_users = users.filter(role='user').count()
        
        # Products
        products = Product.objects.filter(date_filter)
        total_products = products.count()
        
        # Orders
        orders = Order.objects.filter(date_filter)
        total_orders = orders.count()
        revenue_total = orders.aggregate(Sum('total'))['total__sum'] or 0
        avg_ticket = revenue_total / total_orders if total_orders > 0 else 0
        
        # Orders by status
        orders_by_status = list(
            orders.values('status')
            .annotate(count=Count('id'))
            .values('status', 'count')
        )
        orders_by_status_formatted = [
            {'_id': item['status'], 'count': item['count']}
            for item in orders_by_status
        ]
        
        # Carts
        carts = Cart.objects.filter(date_filter)
        total_carts = carts.count()
        
        total_items = sum(cart.items.count() for cart in carts)
        avg_items = total_items / total_carts if total_carts > 0 else 0
        
        conversion_rate = total_orders / total_carts if total_carts > 0 else 0
        
        # Top selling (simplified - would need proper aggregation)
        top_selling = []
        
        return JsonResponse({
            'period': {'start': start.isoformat(), 'end': end.isoformat()},
            'users': {
                'total': total_users,
                'admins': admins,
                'users': normal_users
            },
            'products': {
                'total': total_products,
                'topSelling': top_selling
            },
            'orders': {
                'total': total_orders,
                'revenueTotal': float(revenue_total),
                'avgTicket': float(avg_ticket),
                'byStatus': orders_by_status_formatted
            },
            'carts': {
                'avgItems': avg_items,
                'conversionRate': conversion_rate
            }
        })
        
    except Exception as e:
        print(f"Error generating stats: {e}")
        return JsonResponse(
            {'error': 'Erro ao gerar estatísticas consolidadas'},
            status=500
        )