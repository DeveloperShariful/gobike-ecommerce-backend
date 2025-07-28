# payments/urls.py (FINAL VERSION)

from django.urls import path
from .views import StripePaymentIntentView

app_name = 'payments'

urlpatterns = [
    # API endpoint for creating a Stripe Payment Intent.
    # This will be called by the JavaScript on the checkout page.
    path('stripe/create-payment-intent/', 
         StripePaymentIntentView.as_view(), 
         name='stripe_create_payment_intent'),
    
    # In the future, you can add URLs for PayPal integration, webhooks, etc. here.
    # Example:
    # path('paypal/create-order/', PaypalCreateOrderView.as_view(), name='paypal_create_order'),
    # path('paypal/capture-order/', PaypalCaptureOrderView.as_view(), name='paypal_capture_order'),
]