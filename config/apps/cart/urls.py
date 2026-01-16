from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_cart, name='get_cart'),
    path('add/', views.add_item_to_cart, name='add_item_to_cart'),
    path('remove/', views.remove_item_from_cart, name='remove_item_from_cart'),
    path('clear/', views.clear_cart, name='clear_cart'),
]