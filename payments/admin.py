# payments/admin.py (FINAL VERSION)

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse
from .models import PaymentGateway, Transaction

@admin.register(PaymentGateway)
class PaymentGatewayAdmin(admin.ModelAdmin):
    list_display = ('name', 'processor', 'is_active', 'is_test_mode')
    list_filter = ('is_active', 'is_test_mode', 'processor')
    search_fields = ('name',)
    
    fieldsets = (
        ('Gateway Details', {
            'fields': ('name', 'processor', 'description')
        }),
        ('API Configuration', {
            'fields': ('public_key', 'secret_key'),
            'description': 'Enter the API credentials provided by the payment gateway.'
        }),
        ('Status', {
            'fields': ('is_active', 'is_test_mode')
        }),
    )

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'order_link', 'gateway', 'amount', 'status', 'created_at')
    list_filter = ('status', 'gateway', 'created_at')
    search_fields = ('transaction_id', 'order__order_id_display')
    
    # Make all fields read-only as transactions should be immutable.
    readonly_fields = [field.name for field in Transaction._meta.fields]
    
    def order_link(self, obj):
        if obj.order:
            url = reverse('admin:orders_order_change', args=[obj.order.pk])
            return mark_safe(f'<a href="{url}" target="_blank">{obj.order.order_id_display}</a>')
        return "N/A"
    order_link.short_description = 'Order'

    # Disable add and delete functionality from the admin.
    # Transactions should only be created programmatically.
    def has_add_permission(self, request):
        return False
        
    def has_delete_permission(self, request, obj=None):
        return False
        
    def has_change_permission(self, request, obj=None):
        # Allow viewing but not changing.
        return False