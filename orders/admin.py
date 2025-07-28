# orders/admin.py (FINAL VERSION - UPDATED FOR NEW FEATURES)

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Order, OrderItem, OrderNote, Address, OrderTag, Refund

# ইনলাইন ক্লাসগুলো (OrderItemInline আপডেট করা হয়েছে)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_link', 'variation_info', 'unit_price', 'quantity', 'tax_amount', 'total_price')
    can_delete = False
    
    def product_link(self, obj):
        if obj.product:
            url = reverse('admin:products_product_change', args=[obj.product.pk])
            return mark_safe(f'<a href="{url}" target="_blank">{obj.product.name}</a>')
        return "N/A"
    product_link.short_description = 'Product'

    def variation_info(self, obj):
        if obj.variation:
            attrs = " / ".join([str(attr.value) for attr in obj.variation.attributes.all()])
            return attrs
        return "—"
    variation_info.short_description = 'Variation'
    
    def has_add_permission(self, request, obj=None): return False

class OrderNoteInline(admin.StackedInline):
    model = OrderNote
    extra = 1
    readonly_fields = ('user', 'created_at')
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user": kwargs['initial'] = request.user.id
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class RefundInline(admin.TabularInline):
    model = Refund
    extra = 0
    readonly_fields = ('refunded_by', 'created_at')
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "refunded_by": kwargs['initial'] = request.user.id
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# মূল অর্ডার অ্যাডমিন (UPDATED)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id_display', 'customer_name', 'display_tags', 'status', 'payment_status', 'total', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at', 'tags')
    search_fields = ('order_id_display', 'user__username', 'shipping_address__first_name', 'shipping_address__last_name')
    readonly_fields = (
        'order_id_display', 'user_link', 'subtotal', 'shipping_cost', 'discount_amount', 
        'tax_amount', 'total', 'created_at', 'updated_at', 'tracking_link', 
        'customer_history', 'fraud_analysis'
    )
    inlines = [OrderItemInline, OrderNoteInline, RefundInline]
    actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_completed']
    filter_horizontal = ('tags',)
    autocomplete_fields = ('user', 'shipping_address', 'billing_address', 'coupon', 'shipping_rate') # <-- Autocomplete যোগ করা হয়েছে

    fieldsets = (
        ('Order Actions', {'fields': ('order_actions',)}),
        ('Order Information', {'fields': ('order_id_display', 'user_link', 'tags', 'status', 'payment_status', 'created_at')}),
        ('Customer History', {'classes': ('collapse',), 'fields': ('customer_history',)}),
        ('Fraud Analysis', {'classes': ('collapse',), 'fields': ('fraud_analysis',)}),
        ('Price Summary', {'fields': ('subtotal', 'shipping_cost', 'coupon', 'discount_amount', 'tax_amount', 'total')}), # <-- Coupon 필드 যোগ করা হয়েছে
        ('Payment & Shipping', {'fields': ('payment_method', 'transaction_id', 'shipping_rate', 'tracking_number', 'tracking_url_provider', 'tracking_link')}), # <-- shipping_rate ফিল্ড যোগ করা হয়েছে
        ('Address Information', {'fields': ('shipping_address_details', 'billing_address_details')}),
    )
    
    def get_readonly_fields(self, request, obj=None):
        default_readonly = list(self.readonly_fields)
        if 'order_actions' in default_readonly: default_readonly.remove('order_actions')
        if obj is None: return ('created_at', 'updated_at', 'order_id_display', 'user_link', 'shipping_address_details', 'billing_address_details')
        return default_readonly + ['shipping_address_details', 'billing_address_details']

    def customer_name(self, obj):
        if obj.user: return obj.user.get_full_name() or obj.user.username
        if obj.shipping_address: return f"{obj.shipping_address.first_name} {obj.shipping_address.last_name} (Guest)"
        return "N/A"

    def user_link(self, obj):
        if obj.user:
            url = reverse('admin:auth_user_change', args=[obj.user.pk])
            return mark_safe(f'<a href="{url}" target="_blank">{obj.user.username}</a>')
        return "Guest Order"
    user_link.short_description = 'Customer'
    
    def display_tags(self, obj):
        tags_html = "".join([f'<span style="background-color:{tag.color}; color: #fff; padding: 2px 8px; border-radius: 5px; margin-right: 5px;">{tag.name}</span>' for tag in obj.tags.all()])
        return mark_safe(tags_html)
    display_tags.short_description = 'Tags'
    
    def shipping_address_details(self, obj):
        if obj.shipping_address:
            addr = obj.shipping_address
            return mark_safe(f"{addr.first_name} {addr.last_name}<br>{addr.address_line_1}<br>{addr.city}, {addr.zip_code}<br>{addr.country}<br>Email: {addr.email}<br>Phone: {addr.phone}")
        return "N/A"
    shipping_address_details.short_description = 'Shipping Address'
    
    def billing_address_details(self, obj):
        if obj.billing_address:
            addr = obj.billing_address
            return mark_safe(f"{addr.first_name} {addr.last_name}<br>{addr.address_line_1}<br>{addr.city}, {addr.zip_code}<br>{addr.country}<br>Email: {addr.email}<br>Phone: {addr.phone}")
        return "N/A"
    billing_address_details.short_description = 'Billing Address'

    def tracking_link(self, obj):
        if obj.tracking_number and obj.tracking_url_provider:
            url = obj.tracking_url_provider.format(tracking_number=obj.tracking_number)
            return mark_safe(f'<a href="{url}" target="_blank">{obj.tracking_number}</a>')
        return obj.tracking_number
    tracking_link.short_description = 'Track Shipment'

    def order_actions(self, obj):
        if obj.pk:
            invoice_url = reverse('orders:admin_order_invoice', args=[obj.pk])
            packing_slip_url = reverse('orders:packing_slip', args=[obj.pk])
            return mark_safe(f'<a href="{invoice_url}" class="button" target="_blank">Print Invoice</a>   <a href="{packing_slip_url}" class="button" target="_blank">Print Packing Slip</a>')
        return "Save order to see actions"
    order_actions.short_description = 'Actions'

    def customer_history(self, obj):
        if not obj.user: return "Guest customer."
        order_count = obj.user.orders.count()
        total_spent = sum(o.total for o in obj.user.orders.all() if o.payment_status == 'paid')
        return f"This is the {order_count}th order from this customer. Total spent: ৳{total_spent:,.2f}"
    
    def fraud_analysis(self, obj):
        analysis = []
        if obj.ip_address: analysis.append(f"IP Address: {obj.ip_address}")
        if obj.shipping_address and obj.billing_address and obj.shipping_address.country != obj.billing_address.country:
            analysis.append('<strong style="color: red;">Warning: Shipping and Billing country do not match.</strong>')
        return mark_safe("<br>".join(analysis) or "No data for analysis.")

    @admin.action(description="Mark selected orders as Processing")
    def mark_as_processing(self, request, queryset): queryset.update(status='processing')
    @admin.action(description="Mark selected orders as Shipped")
    def mark_as_shipped(self, request, queryset): queryset.update(status='shipped')
    @admin.action(description="Mark selected orders as Completed")
    def mark_as_completed(self, request, queryset): queryset.update(status='completed')

# Address এবং Tag অ্যাডমিন (Autocomplete-এর জন্য search_fields যোগ করা হয়েছে)
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'city', 'country')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'city', 'address_line_1')

@admin.register(OrderTag)
class OrderTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_color')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    def display_color(self, obj):
        return format_html(f'<div style="width: 20px; height: 20px; background-color: {obj.color}; border-radius: 50%;"></div>')