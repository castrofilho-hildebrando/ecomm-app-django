from django.contrib import admin
from .models import Address

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['street', 'city', 'state', 'user_id', 'is_default']
    list_filter = ['is_default', 'state']
    search_fields = ['street', 'city']