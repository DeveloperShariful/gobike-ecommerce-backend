# orders/urls.py (FINAL VERSION FOR ADMIN ACTIONS)

from django.urls import path
from . import views

# এই URL গুলোকে একটি app_name দেওয়া ভালো অভ্যাস
app_name = 'orders'

urlpatterns = [
    # অ্যাডমিন প্যানেলে PDF ইনভয়েস প্রিন্ট করার জন্য URL
    path('admin/order/<uuid:order_id>/invoice/', 
         views.admin_order_invoice_pdf, 
         name='admin_order_invoice'),
         
    # অ্যাডমিন প্যানেলে প্যাকিং স্লিপ প্রিন্ট করার জন্য URL
    path('admin/order/<uuid:order_id>/packing_slip/', 
         views.admin_packing_slip_pdf, 
         name='packing_slip'),
]