# products/sitemaps.py (FINAL VERSION FOR SEO - PHASE 1)

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product, Category

# ভবিষ্যতে অন্যান্য অ্যাপের মডেল যোগ করা যাবে
# from pages.models import Page 

class ProductSitemap(Sitemap):
    """
    Sitemap for all available products.
    """
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        # শুধুমাত্র is_available=True এবং no_index=False থাকা প্রোডাক্টগুলো সাইটম্যাপে যোগ করা হবে
        return Product.objects.filter(is_available=True, no_index=False)

    def lastmod(self, obj):
        # প্রোডাক্টটি সর্বশেষ কবে আপডেট হয়েছে
        return obj.updated_at
        
    def location(self, obj):
        # ফ্রন্টএন্ডে প্রোডাক্টের URL কেমন হবে
        return f'/products/{obj.slug}'

class CategorySitemap(Sitemap):
    """
    Sitemap for all product categories.
    """
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        # শুধুমাত্র no_index=False থাকা ক্যাটাগরিগুলো সাইটম্যাপে যোগ করা হবে
        return Category.objects.filter(no_index=False)
        
    def location(self, obj):
        # ফ্রন্টএন্ডে ক্যাটাগরির URL কেমন হবে
        return f'/category/{obj.slug}'

# Uncomment and adapt for other apps like a blog or static pages
# class PageSitemap(Sitemap):
#     changefreq = "yearly"
#     priority = 0.5
# 
#     def items(self):
#         return Page.objects.filter(is_published=True, no_index=False)
# 
#     def lastmod(self, obj):
#         return obj.updated_at
# 
#     def location(self, obj):
#         return f'/{obj.slug}'