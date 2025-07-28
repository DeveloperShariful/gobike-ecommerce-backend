# discounts/models.py (FINAL VERSION)

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from products.models import Product, Category

class Coupon(models.Model):
    DISCOUNT_TYPE_CHOICES = (
        ('percentage', 'Percentage Discount'),
        ('fixed_cart', 'Fixed Cart Discount'),
        ('fixed_product', 'Fixed Product Discount'), # For future advanced usage
    )

    code = models.CharField(
        max_length=50, 
        unique=True, 
        help_text="The code customers will enter to get the discount."
    )
    
    discount_type = models.CharField(
        max_length=20, 
        choices=DISCOUNT_TYPE_CHOICES,
        default='percentage'
    )

    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="The value of the discount. For percentage, enter a value like 10 for 10%."
    )
    
    # --- Usage Restrictions ---
    minimum_spend = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="The minimum order amount for the coupon to be valid."
    )
    
    maximum_spend = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="The maximum order amount for the coupon to be valid."
    )

    # Product/Category restrictions
    products = models.ManyToManyField(
        Product, 
        blank=True, 
        help_text="Products this coupon applies to. Leave blank to apply to all products in the cart."
    )
    
    exclude_products = models.ManyToManyField(
        Product, 
        blank=True, 
        related_name='excluded_coupons',
        help_text="Products this coupon should NOT apply to."
    )

    categories = models.ManyToManyField(
        Category, 
        blank=True, 
        help_text="Product categories this coupon applies to."
    )
    
    exclude_categories = models.ManyToManyField(
        Category, 
        blank=True, 
        related_name='excluded_coupons',
        help_text="Product categories this coupon should NOT apply to."
    )

    # --- Usage Limits ---
    usage_limit_per_coupon = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text="How many times this coupon can be used in total. Leave blank for unlimited."
    )
    
    usage_limit_per_user = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text="How many times a single user can use this coupon. Leave blank for unlimited."
    )

    # --- Validity ---
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    
    # --- Tracking ---
    times_used = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"
        ordering = ['-valid_to']