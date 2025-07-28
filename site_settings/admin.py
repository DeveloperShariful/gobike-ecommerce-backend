# site_settings/admin.py (FINAL VERSION)

from django.contrib import admin
from .models import StoreSettings

@admin.register(StoreSettings)
class StoreSettingsAdmin(admin.ModelAdmin):
    # This prevents users from adding new settings objects via the admin.
    # The singleton pattern in the model handles instance creation.
    def has_add_permission(self, request):
        return not StoreSettings.objects.exists()

    # This prevents users from deleting the settings object.
    def has_delete_permission(self, request, obj=None):
        return False

    # Grouping fields for a better user experience in the admin panel.
    fieldsets = (
        ('Store Identity', {
            'fields': ('store_name', 'store_slogan', 'store_logo')
        }),
        ('Store Location & Contact', {
            'fields': (
                'address_line_1', 'address_line_2', 
                'city', 'state', 'zip_code', 'country',
                'support_email', 'support_phone'
            )
        }),
        ('Localization', {
            'fields': ('currency', 'weight_unit', 'dimension_unit'),
            'description': 'Set the default currency and units for your store.'
        }),
        ('Analytics & Tracking', {
            'classes': ('collapse',), # This section will be collapsible
            'fields': ('google_analytics_id', 'facebook_pixel_id'),
            'description': 'Enter your tracking IDs to integrate with analytics services.'
        }),
    )