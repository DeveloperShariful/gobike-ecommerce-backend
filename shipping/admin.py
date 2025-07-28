# shipping/admin.py (CORRECTED VERSION)

from django.contrib import admin
from .models import ShippingZone, ShippingRate

class ShippingRateInline(admin.TabularInline):
    model = ShippingRate
    extra = 1
    fields = ('name', 'method_type', 'rate', 'minimum_order_value', 'is_active')
    ordering = ('rate',)

@admin.register(ShippingZone)
class ShippingZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_countries', 'is_active', 'rate_count')
    search_fields = ('name',)
    list_filter = ('is_active',)
    
    inlines = [ShippingRateInline]
    
    # --- এই লাইনটি ডিলেট বা কমেন্ট আউট করে দিন ---
    # filter_horizontal = ('countries',) 

    def display_countries(self, obj):
        if obj.countries:
            return ", ".join([country.name for country in obj.countries])
        return "All Countries"
    display_countries.short_description = 'Countries / Regions'

    def rate_count(self, obj):
        return obj.rates.count()
    rate_count.short_description = 'Number of Rates'

@admin.register(ShippingRate)
class ShippingRateAdmin(admin.ModelAdmin):
    list_display = ('name', 'zone', 'method_type', 'rate', 'minimum_order_value', 'is_active')
    list_filter = ('zone', 'method_type', 'is_active')
    search_fields = ('name', 'zone__name')
    list_editable = ('rate', 'is_active')
    
    fieldsets = (
        (None, {'fields': ('zone', 'name', 'method_type', 'rate', 'is_active')}),
        ('Conditions', {'classes': ('collapse',), 'fields': ('minimum_order_value', 'maximum_order_value')}),
        ('Additional Information', {'classes': ('collapse',), 'fields': ('description',)})
    )