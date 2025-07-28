# site_settings/models.py (FINAL VERSION)

from django.db import models
from django_countries.fields import CountryField

class StoreSettings(models.Model):
    # --- General Settings ---
    store_name = models.CharField(max_length=100, default="GoBike")
    store_slogan = models.CharField(max_length=255, blank=True)
    store_logo = models.ImageField(upload_to='settings/logo/', blank=True, null=True)

    # --- Store Address ---
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = CountryField()
    
    # --- Contact Information ---
    support_email = models.EmailField(help_text="Email for customer support.")
    support_phone = models.CharField(max_length=20, blank=True)

    # --- Currency Settings ---
    CURRENCY_CHOICES = (
        ('USD', 'US Dollar ($)'),
        ('EUR', 'Euro (€)'),
        ('GBP', 'British Pound (£)'),
        ('BDT', 'Bangladeshi Taka (৳)'),
        ('AUD', 'Australian Dollar (A$)'),
    )
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')

    # --- Units of Measurement ---
    WEIGHT_UNIT_CHOICES = (
        ('kg', 'Kilogram (kg)'),
        ('g', 'Gram (g)'),
        ('lbs', 'Pound (lbs)'),
        ('oz', 'Ounce (oz)'),
    )
    DIMENSION_UNIT_CHOICES = (
        ('m', 'Meter (m)'),
        ('cm', 'Centimeter (cm)'),
        ('mm', 'Millimeter (mm)'),
        ('in', 'Inch (in)'),
        ('yd', 'Yard (yd)'),
    )
    weight_unit = models.CharField(max_length=3, choices=WEIGHT_UNIT_CHOICES, default='kg')
    dimension_unit = models.CharField(max_length=2, choices=DIMENSION_UNIT_CHOICES, default='cm')

    # --- Analytics Integration ---
    google_analytics_id = models.CharField(max_length=50, blank=True, help_text="Your Google Analytics Tracking ID (e.g., UA-12345678-1 or G-XXXXXXXXXX).")
    facebook_pixel_id = models.CharField(max_length=50, blank=True, help_text="Your Facebook Pixel ID.")

    class Meta:
        verbose_name = "Store Settings"
        verbose_name_plural = "Store Settings"
        
    def __str__(self):
        return self.store_name

    # --- Singleton Pattern Implementation ---
    # This ensures only one instance of StoreSettings can be created.
    def save(self, *args, **kwargs):
        self.pk = 1
        super(StoreSettings, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Prevent deletion of the singleton instance
        pass

    @classmethod
    def load(cls):
        # A convenient way to get the settings instance
        obj, created = cls.objects.get_or_create(pk=1)
        return obj