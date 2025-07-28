# site_settings/context_processors.py (NEW FILE)

from .models import StoreSettings
from orders.cart import Cart # আমরা কার্টের তথ্যও গ্লোবালি পাঠাব

def global_settings(request):
    """
    Makes the global store settings and cart available in all templates.
    """
    return {
        'global_settings': StoreSettings.load(),
        'cart': Cart(request),
    }