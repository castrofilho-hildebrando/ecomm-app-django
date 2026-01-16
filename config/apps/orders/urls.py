from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('', views.create_order, name='create_order'),
    path('my/', views.get_my_orders, name='get_my_orders'),
    path('all/', views.get_all_orders, name='get_all_orders'),
    path('<uuid:order_id>/update/', views.update_order_status, name='update_order_status'),
]