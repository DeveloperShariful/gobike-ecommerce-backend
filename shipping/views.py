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
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        if not cart:
            return Response({"error": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        address_data = {
            'zip_code': request.data.get('zip_code'),
            'city': request.data.get('city'),
            'country_code': request.data.get('country_code', 'AU'),
        }

        if not all([address_data['zip_code'], address_data['city'], address_data['country_code']]):
            return Response({"error": "ZIP code, city, and country are required."}, status=status.HTTP_400_BAD_REQUEST)

        # ১. ম্যানুয়াল শিপিং রেট আনা
        manual_rates = self.get_manual_rates(cart, address_data)
        
        # ২. শুধুমাত্র API কী থাকলেই Transdirect থেকে রেট আনা
        real_time_rates = []
        if settings.TRANSDIRECT_API_KEY and settings.TRANSDIRECT_API_KEY != 'your_transdirect_api_key':
            try:
                transdirect_api = TransdirectAPI()
                real_time_rates = transdirect_api.get_quotes(list(cart), address_data)
            except Exception as e:
                print(f"Transdirect API Error: {e}") # সার্ভার লগে এরর দেখা যাবে

        # ৩. সব রেট একত্রিত করা
        all_rates = manual_rates + real_time_rates
        
        if not all_rates:
            # যদি কোনো রেটই না পাওয়া যায়
            return Response([], status=status.HTTP_200_OK)

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