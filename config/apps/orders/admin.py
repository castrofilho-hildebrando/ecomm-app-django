from django.contrib import admin
from .models import Order, OrderItem, Outbox

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'total', 'status', 'created_at']
    list_filter = ['status', 'created_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_id', 'quantity']

@admin.register(Outbox)
class OutboxAdmin(admin.ModelAdmin):
    list_display = ['name', 'processed', 'occurred_at', 'processed_at']
    list_filter = ['processed', 'name']