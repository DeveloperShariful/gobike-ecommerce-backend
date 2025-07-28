# payments/models.py (FINAL VERSION)

from django.db import models
from orders.models import Order

class PaymentGateway(models.Model):
    GATEWAY_PROCESSOR_CHOICES = (
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
        ('cod', 'Cash on Delivery'),
        ('custom', 'Custom Payment'),
    )

    name = models.CharField(max_length=100, help_text="The name of the payment gateway shown to customers.")
    processor = models.CharField(max_length=50, choices=GATEWAY_PROCESSOR_CHOICES, unique=True)
    
    # --- Configuration Fields ---
    # These will be shown in the admin panel to store API keys and other settings.
    # We use encrypted fields in a real-world scenario, but for now, we'll use TextField.
    
    public_key = models.CharField(max_length=255, blank=True, help_text="Public API Key or equivalent.")
    secret_key = models.CharField(max_length=255, blank=True, help_text="Secret API Key or equivalent.")
    
    is_active = models.BooleanField(default=True, help_text="Enable or disable this payment gateway.")
    
    # --- Environment ---
    is_test_mode = models.BooleanField(
        default=True, 
        help_text="Run this gateway in test/sandbox mode. Uncheck for live transactions."
    )
    
    description = models.TextField(
        blank=True, 
        help_text="Description shown to the customer during checkout."
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Payment Gateway"
        verbose_name_plural = "Payment Gateways"

class Transaction(models.Model):
    TRANSACTION_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='transactions')
    gateway = models.ForeignKey(PaymentGateway, on_delete=models.SET_NULL, null=True)
    
    transaction_id = models.CharField(max_length=255, unique=True, help_text="The unique ID from the payment gateway.")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3)
    
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS_CHOICES)
    
    # --- Raw Response ---
    # Storing the full response from the gateway is crucial for debugging.
    raw_response = models.JSONField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transaction {self.transaction_id} for Order {self.order.order_id_display}"

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ['-created_at']