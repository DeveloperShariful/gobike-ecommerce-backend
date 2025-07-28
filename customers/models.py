# customers/models.py (FINAL VERSION)

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomerProfile(models.Model):
    """
    Extends the default Django User model to store customer-specific information.
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='customerprofile'
    )
    
    phone_number = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='customers/profiles/', blank=True, null=True)
    
    # Marketing preferences
    accepts_marketing = models.BooleanField(
        default=True, 
        help_text="Customer agrees to receive marketing emails."
    )

    # Customer notes (for admin use)
    notes = models.TextField(blank=True, help_text="Internal notes about the customer.")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Customer Profile"
        verbose_name_plural = "Customer Profiles"


# --- Signal to automatically create a CustomerProfile when a new User is created ---
@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    """
    This signal ensures that a CustomerProfile is automatically created 
    every time a new Django User is created.
    """
    if created:
        CustomerProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_customer_profile(sender, instance, **kwargs):
    """
    This signal ensures that the profile is saved whenever the User object is saved.
    """
    instance.customerprofile.save()