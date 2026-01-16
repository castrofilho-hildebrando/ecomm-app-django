from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_addresses, name='get_addresses'),
    path('create/', views.create_address, name='create_address'),
    path('<uuid:address_id>/update/', views.update_address, name='update_address'),
    path('<uuid:address_id>/delete/', views.delete_address, name='delete_address'),
]