# shipping/urls.py (NEW FILE)

from django.urls import path
from .views import ShippingOptionsView

app_name = 'shipping'

urlpatterns = [
    # API endpoint for fetching shipping options
    # The front-end will send a POST request to this URL with cart & address data.
    path('options/', ShippingOptionsView.as_view(), name='get_shipping_options'),
]