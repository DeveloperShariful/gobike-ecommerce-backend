# products/urls.py (FINAL VERSION - UPDATED FOR SHOP & CONTACT)

from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Homepage URL
    path('', views.home, name='home'),
    
    # --- নতুন: Shop Page URL ---
    path('shop/', views.shop_view, name='shop'),
    
    # Single Product Detail URL
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Category Page URL
    path('category/<slug:slug>/', views.category_view, name='category_view'),

    # --- ফিক্সড: Contact Form Submit URL ---
    path('contact-submit/', views.contact_submit_view, name='contact_submit'),
    
    # Account Page URL
    path('account/', views.account_view, name='account'),
]