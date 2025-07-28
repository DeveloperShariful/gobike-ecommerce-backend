# customers/admin.py (FINAL VERSION)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import CustomerProfile

# Define an inline admin descriptor for CustomerProfile model
# which acts a bit like a singleton
class CustomerProfileInline(admin.StackedInline):
    model = CustomerProfile
    can_delete = False
    verbose_name_plural = 'Customer Profile'
    fields = ('phone_number', 'profile_picture', 'accepts_marketing', 'notes')

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (CustomerProfileInline,)
    list_display = (
        'username', 
        'email', 
        'first_name', 
        'last_name', 
        'is_staff', 
        'date_joined'
    )
    list_select_related = ('customerprofile',) # Optimizes query to fetch profile data

# Re-register UserAdmin
# First, unregister the default User admin
admin.site.unregister(User)
# Then, register our custom UserAdmin
admin.site.register(User, UserAdmin)

# Optionally, if you want to see Customer Profiles as a separate entry (not recommended for UX)
# @admin.register(CustomerProfile)
# class CustomerProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'phone_number', 'accepts_marketing')