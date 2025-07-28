# discounts/admin.py (FINAL VERSION)

from django.contrib import admin
from .models import Coupon

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'discount_type',
        'amount',
        'is_active',
        'valid_to',
        'times_used',
        'usage_limit_per_coupon'
    )
    list_filter = ('is_active', 'discount_type', 'valid_to')
    search_fields = ('code',)
    
    # These fields will be displayed as read-only.
    readonly_fields = ('times_used',)

    # Using fieldsets to group related fields for a better UX.
    fieldsets = (
        ('General', {
            'fields': (
                'code',
                'discount_type',
                'amount',
                'is_active',
            )
        }),
        ('Usage Restrictions', {
            'classes': ('collapse',),
            'fields': (
                'minimum_spend',
                'maximum_spend',
                'products',
                'exclude_products',
                'categories',
                'exclude_categories',
            ),
            'description': 'Set rules that restrict the use of this coupon.'
        }),
        ('Usage Limits', {
            'classes': ('collapse',),
            'fields': (
                'usage_limit_per_coupon',
                'usage_limit_per_user',
                'valid_from',
                'valid_to',
            ),
            'description': 'Set limits on how many times and when the coupon can be used.'
        }),
    )
    
    # Provides a much better UI for ManyToMany fields.
    filter_horizontal = ('products', 'exclude_products', 'categories', 'exclude_categories')