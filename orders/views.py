# orders/views.py (CORRECTED VERSION WITH ALL CART VIEWS)

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db import transaction

# Models, Cart, etc.
from .models import Order, OrderItem, Address, OrderNote
from products.models import Product, ProductVariation, InventoryLog
from payments.models import PaymentGateway, Transaction
from seo.models import GlobalSEOSettings
from .cart import Cart

# PDF Imports
try: from weasyprint import HTML
except ImportError: HTML = None 

# --- Cart Views ---
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity)
    return redirect('cart:cart_detail')

# --- নতুন: cart_update ভিউ যোগ করা হলো ---
@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart.add(product=product, quantity=quantity, override_quantity=True)
    else:
        cart.remove(product)
    return redirect('cart:cart_detail')

# --- নতুন: cart_remove ভিউ যোগ করা হলো ---
@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')
# ------------------------------------

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'orders/cart.html', {'cart': cart, 'page_title': 'Shopping Cart'})

# --- Checkout View ---
def checkout_view(request): # Renamed to avoid conflict with url name
    cart = Cart(request)
    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('products:home')

    payment_gateways = PaymentGateway.objects.filter(is_active=True)
    stripe_gateway = payment_gateways.filter(processor='stripe').first()
    stripe_pub_key = stripe_gateway.public_key if stripe_gateway else None

    if request.method == 'POST':
        try:
            with transaction.atomic():
                shipping_addr = Address.objects.create(
                    first_name=request.POST.get('first_name'),
                    last_name=request.POST.get('last_name'),
                    email=request.POST.get('email'),
                    phone=request.POST.get('phone'),
                    address_line_1=request.POST.get('address_line_1'),
                    city=request.POST.get('city'),
                    zip_code=request.POST.get('zip_code'),
                    country=request.POST.get('country'),
                )
                billing_addr = shipping_addr

                order = Order.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    shipping_address=shipping_addr,
                    billing_address=billing_addr,
                    subtotal=cart.get_total_price(),
                    shipping_cost=0.00,
                    total=cart.get_total_price(),
                    payment_method=request.POST.get('payment_method'),
                    ip_address=request.META.get('REMOTE_ADDR'),
                )

                for item in cart:
                    product = item['product']
                    OrderItem.objects.create(
                        order=order, product=product,
                        quantity=item['quantity'], unit_price=item['price'],
                    )
                    product.stock_quantity -= item['quantity']
                    product.save()
                    InventoryLog.objects.create(
                        product=product, order=order, change_type='order_placed',
                        change_quantity=-item['quantity'], notes=f"Order #{order.order_id_display}"
                    )
                
                cart.clear()

                if order.payment_method == 'stripe':
                    order.payment_status = 'pending'
                elif order.payment_method == 'cod':
                    order.payment_status = 'pending'
                order.save()

                messages.success(request, f"Thank you! Your order #{order.order_id_display} has been placed.")
                return redirect('products:home')

        except Exception as e:
            print(f"Error creating order: {e}")
            messages.error(request, "There was an error placing your order. Please try again.")

    context = {
        'cart': cart, 'page_title': 'Checkout',
        'payment_gateways': payment_gateways,
        'stripe_publishable_key': stripe_pub_key,
    }
    return render(request, 'orders/checkout.html', context)


# --- PDF Views (অপরিবর্তিত) ---
@staff_member_required
def admin_order_invoice_pdf(request, order_id):
    # ... (code remains the same)
    pass
@staff_member_required
def admin_packing_slip_pdf(request, order_id):
    # ... (code remains the same)
    pass