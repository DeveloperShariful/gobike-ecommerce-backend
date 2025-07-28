# shipping/views.py (FINAL VERSION)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from decimal import Decimal

from orders.cart import Cart
from .models import ShippingRate, ShippingZone
from .transdirect import TransdirectAPI

class ShippingOptionsView(APIView):
    """
    API view to get available shipping options for the current cart.
    It combines manual rates from the database with real-time rates from Transdirect.
    
    Expects a POST request with the following JSON data:
    {
        "zip_code": "2570",
        "city": "Camden South",
        "country_code": "AU"
    }
    """
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        if not cart:
            return Response({"error": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        # --- Extract and validate address data from the POST request ---
        address_data = {
            'zip_code': request.data.get('zip_code'),
            'city': request.data.get('city'),
            'country_code': request.data.get('country_code', 'AU'),
        }

        if not all(address_data.values()):
            return Response({"error": "ZIP code, city, and country are required."}, status=status.HTTP_400_BAD_REQUEST)

        # --- 1. Get Manual Shipping Rates (Free Shipping, Flat Rate, etc.) ---
        try:
            manual_rates = self.get_manual_rates(cart, address_data)
        except Exception as e:
            # In a real app, log this error
            print(f"Error fetching manual rates: {e}")
            manual_rates = []

        # --- 2. Get Real-time Rates from Transdirect ---
        try:
            transdirect_api = TransdirectAPI()
            real_time_rates = transdirect_api.get_quotes(list(cart), address_data)
        except Exception as e:
            # In a real app, log this error
            print(f"Error fetching Transdirect rates: {e}")
            real_time_rates = []
        
        # --- 3. Combine, sort, and return all rates ---
        all_rates = manual_rates + real_time_rates
        
        if not all_rates:
            return Response({"message": "No shipping options available for this address."}, status=status.HTTP_200_OK)

        # Sort rates by price, lowest first
        sorted_rates = sorted(all_rates, key=lambda x: x['price'])
        
        return Response(sorted_rates, status=status.HTTP_200_OK)

    def get_manual_rates(self, cart, address_data):
        """
        Finds applicable manual shipping rates from the database based on zone and conditions.
        """
        cart_total = cart.get_total_price()
        
        # This logic finds the most specific zone first (with country), then falls back to a generic zone.
        # This is a robust way to handle zones.
        zones = ShippingZone.objects.filter(
            Q(countries__contains=address_data['country_code']) | Q(countries__isnull=True) | Q(countries__len=0),
            is_active=True
        ).order_by('-countries') # Prioritize zones with countries specified

        matching_zone = zones.first()

        if not matching_zone:
            return []

        # Find all rates in that zone that meet the order conditions
        applicable_rates = []
        for rate in matching_zone.rates.filter(is_active=True):
            min_spend_ok = (rate.minimum_order_value is None or cart_total >= rate.minimum_order_value)
            max_spend_ok = (rate.maximum_order_value is None or cart_total <= rate.maximum_order_value)
            
            if min_spend_ok and max_spend_ok:
                applicable_rates.append({
                    'name': rate.name,
                    'courier': 'In-House', # To distinguish from API couriers
                    'service_type': rate.method_type,
                    'price': float(rate.rate),
                    'description': rate.description
                })

        return applicable_rates