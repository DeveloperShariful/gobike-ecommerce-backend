# payments/views.py (FINAL VERSION)

import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from orders.cart import Cart

# Set your secret key. Remember to switch to your live secret key in production.
stripe.api_key = settings.STRIPE_SECRET_KEY

class StripePaymentIntentView(APIView):
    """
    API view to create a Stripe Payment Intent.
    """
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        if not cart:
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        
        # --- Calculate the final order amount ---
        # In a real app, this would also include shipping and taxes
        # For now, we'll use the cart's total price.
        # Amount should be in the smallest currency unit (e.g., cents for USD, poisha for BDT).
        
        # Assuming the currency is USD for this example. Change as needed.
        # Stripe expects the amount in cents.
        try:
            amount_in_dollars = cart.get_total_price()
            amount_in_cents = int(amount_in_dollars * 100)

            # --- Create a PaymentIntent with the order amount and currency ---
            intent = stripe.PaymentIntent.create(
                amount=amount_in_cents,
                currency='usd', # Change to your store's currency (e.g., 'aud', 'bdt')
                automatic_payment_methods={
                    'enabled': True,
                },
            )
            
            # --- Send the client secret back to the front-end ---
            return Response({
                'clientSecret': intent.client_secret
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # In a real app, log this error
            print(f"Stripe Error: {e}")
            return Response(
                {'error': 'Something went wrong while creating the payment intent.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )