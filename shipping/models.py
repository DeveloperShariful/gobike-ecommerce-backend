# shipping/models.py (FINAL VERSION)

from django.db import models
from django_countries.fields import CountryField
from products.models import Product

class ShippingZone(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="e.g., Inside Dhaka, USA & Canada")
    countries = CountryField(multiple=True, blank=True, help_text="Select countries for this zone. Leave blank to apply to all countries.")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Shipping Zone"
        verbose_name_plural = "Shipping Zones"

class ShippingRate(models.Model):
    METHOD_TYPE_CHOICES = (
        ('flat_rate', 'Flat Rate'),
        ('free_shipping', 'Free Shipping'),
        ('local_pickup', 'Local Pickup'),
        # Add more types like 'weight_based' in the future if needed
    )

    zone = models.ForeignKey(ShippingZone, on_delete=models.CASCADE, related_name='rates')
    name = models.CharField(max_length=100, help_text="e.g., Standard Delivery, Express Shipping")
    method_type = models.CharField(max_length=20, choices=METHOD_TYPE_CHOICES)
    
    # --- Rate Conditions ---
    rate = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00, 
        help_text="Cost for this shipping method. Set to 0 for Free Shipping."
    )
    
    minimum_order_value = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="This rate will only apply if the order total is above this value."
    )
    
    maximum_order_value = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="This rate will only apply if the order total is below this value."
    )
    
    # --- Additional Settings ---
    description = models.TextField(blank=True, help_text="Optional: A short description shown to the customer at checkout.")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.zone.name} - {self.name}"

    class Meta:
        verbose_name = "Shipping Rate"
        verbose_name_plural = "Shipping Rates"
        ordering = ['zone', 'rate']

# --- Future Advanced Feature: Shipping Classes ---
# This is a placeholder for future expansion if needed.
# class ShippingClass(models.Model):
#     name = models.CharField(max_length=100)
#     slug = models.SlugField(max_length=100, unique=True)
#     description = models.TextField(blank=True)

#     def __str__(self):
#         return self.name

# Add a field in Product model to link ShippingClass:
# shipping_class = models.ForeignKey(ShippingClass, on_delete=models.SET_NULL, null=True, blank=True)