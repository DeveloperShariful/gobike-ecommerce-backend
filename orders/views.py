# orders/views.py (FINAL VERSION FOR PDF GENERATION)

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required

# WeasyPrint PDF জেনারেশনের জন্য
try:
    from weasyprint import HTML
except ImportError:
    HTML = None # যদি WeasyPrint ইনস্টল করা না থাকে

from .models import Order
from seo.models import GlobalSEOSettings # Global SEO সেটিংস থেকে কোম্পানির তথ্য আনার জন্য

@staff_member_required
def admin_order_invoice_pdf(request, order_id):
    """
    অ্যাডমিন প্যানেল থেকে একটি নির্দিষ্ট অর্ডারের জন্য PDF ইনভয়েস তৈরি করে।
    """
    if HTML is None:
        return HttpResponse("WeasyPrint is not installed. Please install it with 'pip install weasyprint'", status=501)

    order = get_object_or_404(Order, id=order_id)
    global_settings = GlobalSEOSettings.load()

    # HTML টেমপ্লেট রেন্ডার করা
    html_string = render_to_string('admin/orders/order_invoice.html', {
        'order': order,
        'global_settings': global_settings
    })

    # HTML থেকে PDF তৈরি করা
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    # HTTP রেসপন্স হিসেবে PDF ফাইল পাঠানো
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=invoice-{order.order_id_display}.pdf'
    
    return response


@staff_member_required
def admin_packing_slip_pdf(request, order_id):
    """
    অ্যাডমিন প্যানেল থেকে একটি নির্দিষ্ট অর্ডারের জন্য PDF প্যাকিং স্লিপ তৈরি করে।
    """
    if HTML is None:
        return HttpResponse("WeasyPrint is not installed. Please install it with 'pip install weasyprint'", status=501)

    order = get_object_or_404(Order, id=order_id)
    global_settings = GlobalSEOSettings.load()

    # HTML টেমপ্লেট রেন্ডার করা
    html_string = render_to_string('admin/orders/packing_slip.html', {
        'order': order,
        'global_settings': global_settings
    })
    
    # HTML থেকে PDF তৈরি করা
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    # HTTP রেসপন্স হিসেবে PDF ফাইল পাঠানো
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=packing-slip-{order.order_id_display}.pdf'
    
    return response