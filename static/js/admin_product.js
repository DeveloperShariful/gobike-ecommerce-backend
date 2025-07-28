// static/js/admin_product.js (FINAL & CORRECTED VERSION 2)

// Django-এর ডিফল্ট jQuery ব্যবহার করা হচ্ছে
if (typeof django !== 'undefined' && typeof django.jQuery !== 'undefined') {
    (function($) {
        $(document).ready(function() {
            function toggleProductTypeFields() {
                var productType = $('#id_product_type').val();
                
                // ভ্যারিয়েশন ইনলাইন (যেটি আইডি দিয়ে শুরু হয়: productvariation_set)
                var variationInline = $('[id^="productvariation_set-"]').closest('.inline-group');
                
                // সিম্পল প্রোডাক্টের ফিল্ডসেট, আমরা CSS ক্লাস দিয়ে টার্গেট করছি
                var simpleProductFieldset = $('.simple-product-fields').closest('fieldset');

                if (productType === 'simple') {
                    simpleProductFieldset.show();
                    if (variationInline.length) {
                        variationInline.hide();
                    }
                } else if (productType === 'variable') {
                    simpleProductFieldset.hide();
                    if (variationInline.length) {
                        variationInline.show();
                    } else {
                        // নতুন প্রোডাক্টের জন্য মেসেজ
                        if ($('.no-variations-message').length === 0) {
                            var lastFieldset = $('fieldset').last();
                            if (lastFieldset.length > 0) {
                                lastFieldset.after('<p class="help no-variations-message" style="margin-left: 130px;"><strong>Note:</strong> Save the product first to add variations.</p>');
                            }
                        }
                    }
                }
            }
            
            // পেজ লোড হওয়ার সাথে সাথে একবার চালানো
            toggleProductTypeFields();
            
            // যখন প্রোডাক্টের ধরন পরিবর্তন করা হবে
            $('#id_product_type').on('change', function() {
                toggleProductTypeFields();
            });
        });
    })(django.jQuery);
}