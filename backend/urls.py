# backend/urls.py (FINAL VERSION - UPDATED FOR ORDERS APP)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

# সাইটম্যাপের জন্য ইম্পোর্ট
from django.contrib.sitemaps.views import sitemap
from products.sitemaps import ProductSitemap, CategorySitemap

# robots.txt ফাইলের জন্য
from seo.models import GlobalSEOSettings

# সাইটম্যাপ অবজেক্টগুলো সংজ্ঞায়িত করা
sitemaps = {
    'products': ProductSitemap,
    'categories': CategorySitemap,
}

# robots.txt ভিউ
def robots_txt(request):
    settings_obj = GlobalSEOSettings.load()
    content = settings_obj.robots_txt_content
    return HttpResponse(content, content_type="text/plain")


urlpatterns = [
    path('admin/', admin.site.urls),

    # --- নতুন: Orders অ্যাপের URL গুলো যোগ করা হলো ---
    path('', include('orders.urls', namespace='orders')),

    # ভবিষ্যতে API-এর জন্য এই লাইনটি Uncomment করতে হবে
    # path('api/v1/', include('products.urls')), 
    
    # SEO URLs
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt),
]

# ডেভেলপমেন্টের সময় মিডিয়া ফাইল সার্ভ করার জন্য
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)