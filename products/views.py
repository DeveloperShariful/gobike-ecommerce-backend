# products/views.py (FINAL VERSION - UPDATED FOR SHOP & CONTACT)

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse # Placeholder-এর জন্য
from .models import Product, Category, ProductReview

# --- Traditional Django Template Views ---

def home(request):
    # হোমপেজে সর্বশেষ ৮টি প্রোডাক্ট দেখানো হচ্ছে
    products = Product.objects.filter(is_available=True).order_by('-created_at')[:8]
    context = {
        'products': products,
        'page_title': 'Welcome to GoBike',
    }
    return render(request, 'products/home.html', context)

# --- নতুন: পূর্ণাঙ্গ Shop Page View ---
def shop_view(request):
    """
    View for the main shop page, displaying all available products with pagination.
    """
    all_products_list = Product.objects.filter(is_available=True).order_by('-created_at')
    
    # Pagination: প্রতি পেজে ১২টি প্রোডাক্ট দেখানো হবে
    paginator = Paginator(all_products_list, 12)
    page_number = request.GET.get('page')
    
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        # যদি page একটি ইন্টিজার না হয়, প্রথম পেজ দেখানো হবে
        products = paginator.page(1)
    except EmptyPage:
        # যদি page সীমার বাইরে হয়, শেষ পেজ দেখানো হবে
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'page_title': 'Shop All Products',
        'meta_description': 'Browse our collection of high-quality electric bikes and accessories.',
    }
    return render(request, 'products/shop.html', context) # এর জন্য আমাদের একটি নতুন টেমপ্লেট লাগবে

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    related_products = product.related_products.filter(is_available=True)[:4]
    reviews = product.reviews.filter(is_approved=True).order_by('-created_at')
    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'page_title': f"{product.name} - GoBike",
        'meta_description': product.meta_description or product.short_description,
    }
    return render(request, 'products/product_detail.html', context)

def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    product_list = Product.objects.filter(category=category, is_available=True)
    
    paginator = Paginator(product_list, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'products': products,
        'page_title': f"{category.name} Products - GoBike",
        'meta_description': category.meta_description or f"Shop for {category.name} at GoBike.",
    }
    return render(request, 'products/category_page.html', context)

# --- Contact Form View (আপডেট করা) ---
def contact_submit_view(request):
    if request.method == 'POST':
        # এখানে ফর্ম থেকে ডেটা প্রসেস করার লজিক থাকবে।
        # যেমন: ডেটাবেসে সেভ করা বা অ্যাডমিনকে ইমেইল পাঠানো।
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # আপাতত, আমরা শুধু একটি সফল বার্তা দেখাব।
        # প্রোডাকশনে এখানে SendGrid বা অন্য কোনো সার্ভিস দিয়ে ইমেইল পাঠানো হবে।
        success_message = f"Thank you, {name}! Your message has been received. We will contact you at {email} soon."
        
        # আমরা একটি নতুন টেমপ্লেট রেন্ডার করতে পারি অথবা মেসেজ ফ্রেেমওয়ার্ক ব্যবহার করতে পারি।
        # সহজ সমাধানের জন্য, HttpResponse ব্যবহার করা হলো।
        return HttpResponse(success_message, status=200)

    # যদি কেউ GET রিকোয়েস্ট দিয়ে এই URL-এ আসে, তাকে হোমপেজে পাঠিয়ে দেওয়া হবে।
    return redirect('products:home')

# --- Account Page View (placeholder) ---
def account_view(request):
    # ভবিষ্যতে এখানে কাস্টমার লগইন/রেজিস্ট্রেশন এবং ড্যাশবোর্ড থাকবে।
    context = {'page_title': 'My Account'}
    return render(request, 'customers/account.html', context) # এর জন্য নতুন টেমপ্লেট লাগবে