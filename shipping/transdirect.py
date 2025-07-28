# shipping/transdirect.py (NEW FILE - COMPLETE API LOGIC)

import requests
from django.conf import settings

class TransdirectAPI:
    """
    A wrapper for the Transdirect API to handle quotes, bookings, and custom business logic.
    """
    def __init__(self):
        self.api_key = settings.TRANSDIRECT_API_KEY
        self.base_url = "https://api.transdirect.com.au/v1"
        self.headers = {
            "Authorization": f"Basic {self.api_key}",
            "Content-Type": "application/json"
        }

    def _make_request(self, method, endpoint, data=None):
        """
        Helper method to make requests to the Transdirect API.
        """
        url = f"{self.base_url}{endpoint}"
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=self.headers, params=data)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=self.headers, json=data)
            else:
                return {'error': 'Unsupported HTTP method'}

            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            return response.json()
        
        except requests.exceptions.RequestException as e:
            # In a real app, log this error
            print(f"Transdirect API Error: {e}")
            return {'error': str(e)}

    def get_quotes(self, cart_items, shipping_address):
        """
        Fetch real-time shipping quotes from Transdirect based on cart and address.
        """
        items_payload = []
        for item in cart_items:
            product = item['product']
            items_payload.append({
                "weight": float(product.weight) if product.weight else 0.1,
                "height": float(product.height) if product.height else 10,
                "width": float(product.width) if product.width else 10,
                "length": float(product.length) if product.length else 10,
                "quantity": item['quantity'],
                "item_type": "carton"
            })

        payload = {
            "declared_value": sum(float(item['total_price']) for item in cart_items),
            "referrer": "GoBike Custom Integration",
            "pickup": {"country": "AU"}, # Assuming pickup from a fixed location in Australia
            "delivery": {
                "type": "business" if 'company' in shipping_address else "residential",
                "postcode": shipping_address.get('zip_code'),
                "suburb": shipping_address.get('city'),
                "country": shipping_address.get('country_code', 'AU')
            },
            "items": items_payload
        }
        
        response = self._make_request('POST', '/quotes', data=payload)
        
        if 'error' in response or 'quotes' not in response:
            return [] # Return empty list if there's an error

        return self._apply_business_logic(response['quotes'], shipping_address)

    def _apply_business_logic(self, quotes, shipping_address):
        """
        Apply custom handling fees, markups, and conditional logic.
        """
        processed_quotes = []

        # --- Business Logic Settings (these would come from a model in a real app) ---
        handling_fee = 5.00  # Example: ৳5.00 flat handling fee
        local_pickup_postcodes = ['2570', '2560'] # Example postcodes for local pickup
        
        # --- Conditional Local Pickup ---
        if shipping_address.get('zip_code') in local_pickup_postcodes:
            processed_quotes.append({
                'name': 'Local Pickup',
                'courier': 'GoBike Store',
                'service_type': 'pickup',
                'price': 0.00,
                'description': 'Pick up your order directly from our store.'
            })

        for quote in quotes:
            price = float(quote.get('total', 0))
            
            # --- General Handling Fee ---
            price += handling_fee

            # --- Conditional Dynamic Markup ---
            # Example: Add a 10% markup for "TNT" courier
            if quote.get('courier', '').lower() == 'tnt':
                price *= 1.10
            
            # Example: Add a flat ৳2.00 extra for "Express" services
            if 'express' in quote.get('service_type', '').lower():
                price += 2.00
                
            processed_quotes.append({
                'name': f"{quote.get('courier')} - {quote.get('service_type').replace('_', ' ').title()}",
                'courier': quote.get('courier'),
                'service_type': quote.get('service_type'),
                'price': round(price, 2),
                'description': f"Estimated delivery: {quote.get('etd_display', 'N/A')}"
            })
            
        return sorted(processed_quotes, key=lambda x: x['price'])

    def create_booking(self, order):
        """
        Syncs a Django order with Transdirect's "Orders" tab by creating a booking.
        """
        shipping_addr = order.shipping_address
        items_payload = [{
            "weight": float(item.product.weight or 0.1),
            "height": float(item.product.height or 10),
            "width": float(item.product.width or 10),
            "length": float(item.product.length or 10),
            "quantity": item.quantity,
            "description": item.product.name
        } for item in order.items.all()]

        payload = {
            "ordered_by": order.user.get_full_name() if order.user else f"{shipping_addr.first_name} {shipping_addr.last_name}",
            "confirmation_email": shipping_addr.email,
            "delivery": {
                "name": f"{shipping_addr.first_name} {shipping_addr.last_name}",
                "address": shipping_addr.address_line_1,
                "suburb": shipping_addr.city,
                "postcode": shipping_addr.zip_code,
                "phone": shipping_addr.phone,
                "country": "AU",
            },
            "items": items_payload,
            # Add other required fields like pickup address
        }

        # This endpoint books the shipment.
        # For just syncing to "Orders", you might use a different endpoint or parameter.
        # This is a simplified example.
        return self._make_request('POST', '/bookings', data=payload)