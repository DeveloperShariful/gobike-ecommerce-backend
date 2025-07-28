# orders/models.py (FINAL VERSION - UPDATED FOR NEW FEATURES)

import uuid
from django.db import models
from django.conf import settings
from products.models import Product, ProductVariation
from django.contrib.auth.models import User
from discounts.models import Coupon # <-- নতুন: Coupon মডেল ইম্পোর্ট
from shipping.models import ShippingRate # <-- নতুন: ShippingRate মডেল ইম্পোর্ট

# OrderTag Model (অপরিবর্তিত)
class OrderTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    color = models.CharField(max_length=7, default="#DDDDDD", help_text="Hex color code, e.g., #FF5733")
    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.slug: self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self): return self.name

# Address Model (অপরিবর্তিত)
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "Addresses"
    def __str__(self): return f"{self.first_name} {self.last_name} - {self.address_line_1}"

# মূল অর্ডার মডেল (UPDATED)
class Order(models.Model):
    ORDER_STATUS_CHOICES = (('pending', 'Pending'), ('processing', 'Processing'), ('shipped', 'Shipped'), ('completed', 'Completed'), ('cancelled', 'Cancelled'), ('refunded', 'Refunded'), ('failed', 'Failed'))
    PAYMENT_STATUS_CHOICES = (('pending', 'Pending'), ('paid', 'Paid'), ('failed', 'Failed'))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_id_display = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    
    shipping_address = models.ForeignKey(Address, related_name='shipping_orders', on_delete=models.SET_NULL, null=True, blank=True)
    billing_address = models.ForeignKey(Address, related_name='billing_orders', on_delete=models.SET_NULL, null=True, blank=True)
    
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # --- নতুন/আপডেট করা ফিল্ড ---
    shipping_rate = models.ForeignKey(ShippingRate, on_delete=models.SET_NULL, null=True, blank=True)
    shipping_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    # ---------------------------

    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    payment_method = models.CharField(max_length=100, blank=True)
    transaction_id = models.CharField(max_length=255, blank=True)
    
    # --- shipping_method ফিল্ডটি shipping_rate দ্বারা প্রতিস্থাপিত হয়েছে ---
    # shipping_method = models.CharField(max_length=100, blank=True)
    
    tracking_number = models.CharField(max_length=255, blank=True)
    tracking_url_provider = models.CharField(max_length=2000, blank=True, help_text="URL template for tracking. Use {tracking_number} as a placeholder.")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    tags = models.ManyToManyField(OrderTag, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_id_display:
            last_order = Order.objects.order_by('created_at').last()
            new_id = 1001 if not last_order else int(last_order.order_id_display.split('-')[1]) + 1
            self.order_id_display = f"GO-{new_id}"
        super().save(*args, **kwargs)

    def __str__(self): return self.order_id_display

# অর্ডার আইটেম মডেল (UPDATED)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    variation = models.ForeignKey(ProductVariation, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    
    # --- নতুন: Tax Amount per item ---
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    # -----------------------------
    
    total_price = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    def __str__(self):
        item_name = self.product.name if self.product else "Deleted Product"
        if self.variation:
            attrs = " / ".join([str(attr.value) for attr in self.variation.attributes.all()])
            return f"{self.quantity} x {item_name} ({attrs})"
        return f"{self.quantity} x {item_name}"

    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)

# OrderNote Model (অপরিবর্তিত)
class OrderNote(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='notes')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.TextField()
    is_customer_note = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
    def __str__(self): return f"Note for Order {self.order.order_id_display}"

# Refund Model (অপরিবর্তিত)
class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='refunds')
    refunded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.TextField()
    restock_items = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"Refund of {self.amount} for Order {self.order.order_id_display}"