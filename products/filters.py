# products/filters.py (NEW FILE)

import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    # দাম অনুযায়ী ফিল্টার
    price = django_filters.RangeFilter(field_name='regular_price')

    # ছবি আছে কি নেই
    has_image = django_filters.BooleanFilter(field_name='featured_image', lookup_expr='isnull', exclude=True)

    class Meta:
        model = Product
        fields = {
            'category': ['exact'],
            'tags': ['exact'],
            'product_type': ['exact'],
            'is_available': ['exact'],
            'stock_quantity': ['lt', 'gt'], # Less than, Greater than
        }