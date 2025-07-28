# seo/admin.py (FINAL VERSION FOR SEO - PHASE 1)

from django.contrib import admin
from .models import Redirect, GlobalSEOSettings

@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    list_display = ('source_url', 'target_url', 'redirect_type', 'is_active', 'updated_at')
    list_filter = ('redirect_type', 'is_active')
    search_fields = ('source_url', 'target_url')
    list_editable = ('is_active',)


@admin.register(GlobalSEOSettings)
class GlobalSEOSettingsAdmin(admin.ModelAdmin):
    # এই মডেলে একটি মাত্র অবজেক্ট থাকবে, তাই তালিকা পেজের কোনো প্রয়োজন নেই।
    # আমরা সরাসরি চেঞ্জ পেজে নিয়ে যাব।
    def has_add_permission(self, request):
        # একটির বেশি অবজেক্ট তৈরি করতে দেবে না
        return not GlobalSEOSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # অবজেক্ট ডিলেট করতে দেবে না
        return False

    fieldsets = (
        ('Organization Schema', {
            'description': "This information is used for Google's Knowledge Graph and other structured data.",
            'fields': ('organization_name', 'organization_logo', 'organization_url', 'contact_phone', 'contact_email', 'address')
        }),
        ('robots.txt', {
            'description': "Control how search engines crawl your site. Be very careful with these settings.",
            'fields': ('robots_txt_content',)
        }),
    )