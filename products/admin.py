# products/admin.py (FINAL VERSION WITH SEO FIELDS)

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db import models
from ckeditor.widgets import CKEditorWidget
from import_export.admin import ImportExportModelAdmin
from .models import (
    Category, Tag, Product, ProductImage, 
    Attribute, AttributeValue, ProductVariation, ProductReview,
    ProductSpecification, InventoryLog
)

# ইনলাইন ক্লাসগুলো (অপরিবর্তিত)
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('image_preview',)
    def image_preview(self, obj):
        if obj.image and hasattr(obj.image, 'url'): return format_html(f'<img src="{obj.image.url}" style="max-width: 150px; max-height: 150px; object-fit: cover;" />')
        return "Save to see preview"
    image_preview.short_description = 'Preview'

class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    extra = 0
    autocomplete_fields = ('attributes',)

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1

class InventoryLogInline(admin.TabularInline):
    model = InventoryLog
    extra = 0
    readonly_fields = ('change_type', 'change_quantity', 'notes', 'timestamp', 'changed_by')
    can_delete = False
    def has_add_permission(self, request, obj=None): return False


# মূল প্রোডাক্ট অ্যাডমিন
@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    formfield_overrides = {models.TextField: {'widget': CKEditorWidget(config_name='default')}}
    
    list_display = ('name', 'get_featured_image', 'product_type', 'category', 'is_available')
    list_filter = ('product_type', 'category', 'is_available', 'tags')
    search_fields = ('name', 'sku', 'category__name')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'get_frontend_url')
    filter_horizontal = ('tags', 'related_products', 'upsell_products', 'cross_sell_products')
    actions = ['make_available', 'make_unavailable', 'duplicate_selected_products']
    
    class Media:
        js = ('js/admin_product.js',)

    fieldsets = (
        (None, {'fields': ('product_type', 'name', 'slug', 'get_frontend_url')}),
        ('Content', {'fields': ('description', 'short_description')}),
        
        # --- নতুন: SEO এবং Social Media সেকশন ---
        ('Search Engine Optimization', {
            'classes': ('collapse',),
            'fields': ('seo_title', 'meta_description', 'focus_keyword', 'canonical_url', 'no_index', 'no_follow'),
            'description': 'These fields control how the product appears in search results.'
        }),
        ('Social Media', {
            'classes': ('collapse',),
            'fields': ('og_title', 'og_description', 'og_image'),
            'description': 'These fields control how the product appears when shared on social media.'
        }),
        # ------------------------------------

        ('Organization', {'fields': ('category', 'tags')}),
        ('Images', {'fields': ('featured_image',)}),
        ('Pricing & Inventory (for Simple Products)', {'fields': ('regular_price', 'sale_price', 'sku', 'stock_quantity'), 'classes': ('simple-product-fields',)}),
        ('Shipping Information', {'classes': ('collapse',), 'fields': ('weight', 'length', 'width', 'height')}),
        ('Marketing', {'classes': ('collapse',), 'fields': ('related_products', 'upsell_products', 'cross_sell_products')}),
        ('Status', {'fields': ('manage_stock', 'is_available')}),
        ('Timestamps', {'classes': ('collapse',), 'fields': ('created_at', 'updated_at')})
    )
    
    def get_inlines(self, request, obj=None):
        inlines = [ProductSpecificationInline, ProductImageInline]
        if obj: inlines.append(InventoryLogInline)
        if obj and obj.product_type == 'variable': inlines.append(ProductVariationInline)
        return inlines

    def get_featured_image(self, obj):
        if obj.featured_image and hasattr(obj.featured_image, 'url'): return format_html(f'<img src="{obj.featured_image.url}" style="max-width: 60px; max-height: 60px; object-fit: cover;" />')
        return "No Image"
    get_featured_image.short_description = 'Image'

    def get_frontend_url(self, obj):
        if obj.slug:
            url = f"http://localhost:3000/products/{obj.slug}"
            return mark_safe(f'<a href="{url}" target="_blank">{url}</a>')
        return "Save to generate link"
    get_frontend_url.short_description = 'Frontend URL'

    @admin.action(description="Mark selected products as Available")
    def make_available(self, request, queryset):
        queryset.update(is_available=True)

    @admin.action(description="Mark selected products as Unavailable")
    def make_unavailable(self, request, queryset):
        queryset.update(is_available=False)
        
    @admin.action(description="Duplicate selected products")
    def duplicate_selected_products(self, request, queryset):
        for obj in queryset:
            tags = list(obj.tags.all())
            related = list(obj.related_products.all())
            upsell = list(obj.upsell_products.all())
            cross_sell = list(obj.cross_sell_products.all())
            
            original_sku = obj.sku
            
            obj.pk = None
            obj.slug = f"{obj.slug}-copy"
            obj.name = f"{obj.name} (Copy)"

            if original_sku:
                import time
                timestamp = int(time.time() * 1000)
                obj.sku = f"{original_sku}-copy-{timestamp}"
            
            obj.save()

            obj.tags.set(tags)
            obj.related_products.set(related)
            obj.upsell_products.set(upsell)
            obj.cross_sell_products.set(cross_sell)
            
        self.message_user(request, f"{queryset.count()} product(s) have been successfully duplicated.")
# ক্যাটাগরি অ্যাডমিন (SEO ফিল্ড সহ)
@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('name', 'slug', 'parent')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'parent', 'image')}),
        ('Content', {'fields': ('description',)}),
        # --- নতুন: SEO সেকশন ---
        ('Search Engine Optimization', {
            'classes': ('collapse',),
            'fields': ('seo_title', 'meta_description', 'focus_keyword', 'canonical_url', 'no_index', 'no_follow'),
        }),
        ('Social Media', {
            'classes': ('collapse',),
            'fields': ('og_title', 'og_description', 'og_image'),
        }),
    )

# --- অন্যান্য অ্যাডমিন ক্লাস অপরিবর্তিত ---
@admin.register(Tag)
class TagAdmin(ImportExportModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('attribute', 'value', 'get_swatch')
    list_filter = ('attribute',)
    search_fields = ('value',)
    autocomplete_fields = ('attribute',)

    def get_swatch(self, obj):
        if obj.color_code: return format_html(f'<div style="width: 20px; height: 20px; background-color: {obj.color_code}; border: 1px solid #ccc;"></div>')
        if obj.image_swatch and hasattr(obj.image_swatch, 'url'): return format_html(f'<img src="{obj.image_swatch.url}" style="width: 25px; height: 25px;" />')
        return "N/A"
    get_swatch.short_description = 'Swatch Preview'

@admin.register(ProductReview)
class ProductReviewAdmin(ImportExportModelAdmin):
    list_display = ('product', 'user', 'rating', 'is_approved')
    list_filter = ('is_approved', 'rating')
    search_fields = ('product__name', 'user__username')
    
@admin.register(InventoryLog)
class InventoryLogAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'change_type', 'change_quantity', 'changed_by')
    list_filter = ('change_type', 'timestamp')
    readonly_fields = [f.name for f in InventoryLog._meta.fields]
    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False