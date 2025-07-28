# backend/urls.py (FINAL VERSION - CONNECTS ALL APPS AND APIs)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

# সাইটম্যাপ এবং robots.txt-এর জন্য ইম্পোর্ট
from django.contrib.sitemaps.views import sitemap
from products.sitemaps import ProductSitemap, CategorySitemap
from seo.models import GlobalSEOSettings

# orders.urls থেকে আলাদা URL গ্রুপগুলো ইম্পোর্ট করা হচ্ছে
from orders.urls import admin_urlpatterns, checkout_urlpatterns

# সাইটম্যাপ অবজেক্ট
sitemaps = {
    'products': ProductSitemap,
    'categories': CategorySitemap,
}

# robots.txt ভিউ
def robots_txt(request):
    settings_obj = GlobalSEOSettings.load()
    return HttpResponse(settings_obj.robots_txt_content, content_type="text/plain")


urlpatterns = [
    # 1. Admin Panel
    path('admin/', admin.site.urls),

    # 2. API Endpoints
    # All API URLs will be prefixed with /api/v1/
    path('api/v1/', include([
        path('shipping/', include('shipping.urls', namespace='shipping_api')),
        path('payments/', include('payments.urls', namespace='payments_api')),
        # Future API endpoints for products, orders etc. will go here
    ])),
    
    # 3. Cart URLs (namespaced under 'cart')
    path('', include('orders.urls', namespace='cart')),
    
    # 4. Checkout and Admin PDF URLs (not namespaced)
    path('', include(checkout_urlpatterns)),
    path('', include(admin_urlpatterns)),
    
    # 5. Product, Home, and other page URLs (namespaced under 'products')
    # This should be the last one as it includes the root URL ('')
    path('', include('products.urls', namespace='products')),
    
    # 6. SEO URLs
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt),
]

# ডেভেলপমেন্টের সময় মিডিয়া এবং স্ট্যাটিক ফাইল সার্ভ করার জন্য
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)