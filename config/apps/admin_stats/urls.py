from django.urls import path
from . import views

urlpatterns = [
    path('stats/', views.get_stats, name='get_stats'),
]