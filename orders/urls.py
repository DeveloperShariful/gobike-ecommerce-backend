# orders/urls.py (CORRECTED VERSION)

from django.urls import path
from . import views

# Cart-এর জন্য আলাদা namespace
app_name = 'cart'

urlpatterns = [
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
]

# --- Admin PDF URLs ---
# এই URL গুলো আলাদাভাবে মূল urls.py-তে যোগ করা হবে, namespace ছাড়া।
admin_urlpatterns = [
    path('admin/order/<uuid:order_id>/invoice/', views.admin_order_invoice_pdf, name='admin_order_invoice'),
    path('admin/order/<uuid:order_id>/packing_slip/', views.admin_packing_slip_pdf, name='packing_slip'),
]

# --- Checkout URL ---
# এটিও আলাদাভাবে মূল urls.py-তে যোগ করা হবে।
# orders/urls.py

# ...
checkout_urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'), # <-- checkout কে checkout_view করা হয়েছে
]