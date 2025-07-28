# analytics/admin.py (FINAL & CLEANEST VERSION)

from django.contrib import admin
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

# ডেটা মডেলগুলো ইম্পোর্ট করা
from orders.models import Order
from products.models import Product

# Django-এর ডিফল্ট অ্যাডমিন সাইটের index view-কে আমরা সরাসরি ওভাররাইড করব
# এটি Django-এর একটি স্বীকৃত এবং শক্তিশালী পদ্ধতি

# প্রথমে, ডিফল্ট index view-টিকে একটি ভেরিয়েবলে সংরক্ষণ করা হচ্ছে
original_index = admin.site.index

def analytics_dashboard_index(request, extra_context=None):
    """
    This is our custom index view that will replace the default admin index.
    It calculates analytics data and passes it to the admin/index.html template.
    """
    
    # --- ডেটা ক্যালকুলেশন ---
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    # শুধুমাত্র 'paid' স্ট্যাটাসের অর্ডারগুলোকে সেলস হিসেবে গণনা করা হচ্ছে
    paid_orders = Order.objects.filter(payment_status='paid')

    # সেলস পরিসংখ্যান
    total_sales = paid_orders.aggregate(total=Sum('total'))['total'] or 0
    sales_today = paid_orders.filter(created_at__date=today).aggregate(total=Sum('total'))['total'] or 0
    sales_this_week = paid_orders.filter(created_at__gte=start_of_week).aggregate(total=Sum('total'))['total'] or 0
    sales_this_month = paid_orders.filter(created_at__gte=start_of_month).aggregate(total=Sum('total'))['total'] or 0
    
    # অর্ডার পরিসংখ্যান
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    processing_orders = Order.objects.filter(status='processing').count()

    # প্রোডাক্ট পরিসংখ্যান
    low_stock_products = Product.objects.filter(manage_stock=True, stock_quantity__lte=5, is_available=True).order_by('stock_quantity')[:5]
    
    # সাম্প্রতিক অর্ডার
    recent_orders = Order.objects.order_by('-created_at')[:5]

    # টেমপ্লেটের জন্য context তৈরি করা
    context = {
        'dashboard_title': 'Store Analytics Dashboard',
        'sales_stats': {
            'total': f"৳{total_sales:,.2f}",
            'today': f"৳{sales_today:,.2f}",
            'this_week': f"৳{sales_this_week:,.2f}",
            'this_month': f"৳{sales_this_month:,.2f}",
        },
        'order_stats': {
            'total': total_orders,
            'pending': pending_orders,
            'processing': processing_orders,
        },
        'low_stock_products': low_stock_products,
        'recent_orders': recent_orders,
    }

    # যদি extra_context থাকে, তাহলে সেটিকে আমাদের context-এর সাথে যোগ করা
    if extra_context:
        context.update(extra_context)
        
    # মূল index view-কে কল করা, কিন্তু আমাদের নিজস্ব context এবং টেমপ্লেট দিয়ে
    # Django স্বয়ংক্রিয়ভাবে `templates/admin/index.html` টেমপ্লেটটি ব্যবহার করবে
    return original_index(request, context)


# আমাদের নতুন analytics_dashboard_index ফাংশনটিকে ডিফল্ট অ্যাডমিন সাইটের index হিসেবে সেট করা
admin.site.index = analytics_dashboard_index