from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_users, name='get_all_users'),
    path('<uuid:user_id>/', views.get_user_by_id, name='get_user_by_id'),
    path('<uuid:user_id>/update/', views.update_user, name='update_user'),
    path('<uuid:user_id>/delete/', views.delete_user, name='delete_user'),
]