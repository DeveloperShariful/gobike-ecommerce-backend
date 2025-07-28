# products/models.py (FINAL VERSION WITH ALL SEO FEATURES)

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.urls import reverse

# --- নতুন: Tax Class Model ---
class TaxClass(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="e.g., Standard Rate, Zero Rate")
    rate_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Tax rate in percentage. e.g., 15 for 15%."
    )

    class Meta:
        verbose_name = "Tax Class"
        verbose_name_plural = "Tax Classes"

    def __str__(self):
        return f"{self.name} ({self.rate_percentage}%)"

# SEO-এর জন্য একটি অ্যাবস্ট্রাক্ট মডেল (যাতে কোড পুনরায় ব্যবহার করা যায়)
class SEOModel(models.Model):
    seo_title = models.CharField(
        max_length=60, 
        blank=True, 
        help_text="Optimal length: 50-60 characters. Leave blank to use the item's name."
    )
    meta_description = models.CharField(
        max_length=160, 
        blank=True, 
        help_text="Optimal length: 150-160 characters. Leave blank to use the item's description."
    )
    focus_keyword = models.CharField(max_length=255, blank=True)
    
    # Social Media Optimization
    og_title = models.CharField(max_length=255, blank=True, help_text="Title for social media sharing.")
    og_description = models.TextField(blank=True, help_text="Description for social media sharing.")
    og_image = models.ImageField(upload_to='seo/og/', blank=True, null=True, help_text="Image for social media sharing (e.g., 1200x630px).")
    
    # Indexing Control
    canonical_url = models.URLField(blank=True, help_text="The canonical URL for this page.")
    no_index = models.BooleanField(default=False, help_text="Ask search engines not to index this page.")
    no_follow = models.BooleanField(default=False, help_text="Ask search engines not to follow links on this page.")

    class Meta:
        abstract = True


# ১. ক্যাটাগরি মডেল (SEOModel ব্যবহার করছে)
class Category(SEOModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.name)
        if not self.seo_title: self.seo_title = self.name
        if not self.meta_description and self.description: self.meta_description = self.description[:160]
        super().save(*args, **kwargs)

    def __str__(self): return self.name

# ২. ট্যাগ মডেল (অপরিবর্তিত)
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self): return self.name

# ৩. মূল প্রোডাক্ট মডেল (SEOModel ব্যবহার করছে)
#Product Model (UPDATED)
class Product(SEOModel):
    PRODUCT_TYPE_CHOICES = (('simple', 'Simple'), ('variable', 'Variable'))
    BACKORDER_CHOICES = (
        ('no', 'Do not allow'),
        ('notify', 'Allow, but notify customer'),
        ('yes', 'Allow'),
    )

    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPE_CHOICES, default='simple')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    short_description = models.TextField(blank=True)
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)
    category = models.ForeignKey('Category', related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='products')
    regular_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    tax_class = models.ForeignKey('TaxClass', on_delete=models.SET_NULL, null=True, blank=True)

    stock_quantity = models.IntegerField(default=0)
    manage_stock = models.BooleanField(default=True)
    
    allow_backorders = models.CharField(max_length=10, choices=BACKORDER_CHOICES, default='no')

    is_available = models.BooleanField(default=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    length = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    width = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    featured_image = models.ImageField(upload_to='products/featured/', blank=True, null=True)
    related_products = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='related_to')
    upsell_products = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='upsold_by')
    cross_sell_products = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='cross_sold_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.name)
        if not self.seo_title: self.seo_title = self.name
        if not self.meta_description: self.meta_description = self.short_description[:160]
        super().save(*args, **kwargs)
        
    def __str__(self): 
        return self.name

    # --- নতুন: get_absolute_url মেথড ---
    def get_absolute_url(self):
        """
        Returns the canonical URL for a product instance.
        This is used in templates with {% url 'products:product_detail' product.slug %}.
        """
        return reverse('products:product_detail', args=[self.slug])

# ৪. প্রোডাক্ট গ্যালারি ছবি (অপরিবর্তিত)
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='gallery_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=255, blank=True, help_text="Important for Image SEO.")
    def __str__(self): return f"Image for {self.product.name}"

# ৫. অ্যাট্রিবিউটস (অপরিবর্তিত)
class Attribute(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.name
class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, related_name='values', on_delete=models.CASCADE)
    value = models.CharField(max_length=100)
    color_code = models.CharField(max_length=7, blank=True, help_text="e.g., #FF5733")
    image_swatch = models.ImageField(upload_to='swatches/', blank=True, null=True)
    class Meta:
        unique_together = ('attribute', 'value')
    def __str__(self): return f"{self.attribute.name}: {self.value}"

# ৬. ProductVariation Model (UPDATED)
class ProductVariation(models.Model):
    product = models.ForeignKey(Product, related_name='variations', on_delete=models.CASCADE, limit_choices_to={'product_type': 'variable'})
    attributes = models.ManyToManyField(AttributeValue, related_name='variations')
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)
    stock_quantity = models.IntegerField(default=0)
    
    # --- নতুন: Backorder ---
    allow_backorders = models.CharField(max_length=10, choices=Product.BACKORDER_CHOICES, default='no')
    # -----------------------

    image = models.ForeignKey(ProductImage, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        attrs = " / ".join([str(attr.value) for attr in self.attributes.all()])
        return f"{self.product.name} ({attrs})"

# ৭. প্রোডাক্ট রিভিউ (অপরিবর্তিত)
class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
        unique_together = ('product', 'user')
    def __str__(self): return f"Review for '{self.product.name}' by {self.user.username}"

# ৮. প্রোডাক্ট স্পেসিফিকেশন (অপরিবর্তিত)
class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=255)
    class Meta:
        verbose_name = "Product Specification"
        verbose_name_plural = "Product Specifications"
        unique_together = ('product', 'name')
    def __str__(self): return f"{self.name}: {self.value}"

# ৯. ইনভেন্টরি লগ (অপরিবর্তিত)
# InventoryLog Model (UPDATED)
class InventoryLog(models.Model):
    CHANGE_TYPE_CHOICES = (('order_placed', 'Order Placed'), ('stock_added', 'Stock Added'), ('return', 'Return'), ('manual_edit', 'Manual Edit'))
    
    # --- নতুন: Order মডেল ইম্পোর্ট করা হয়েছে ---
    # models.ForeignKey-এ স্ট্রিং ('orders.Order') ব্যবহার করা হচ্ছে যাতে Circular Import Error না হয়
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, related_name='inventory_changes', null=True, blank=True)
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory_logs', null=True, blank=True)
    variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, related_name='inventory_logs', null=True, blank=True)
    change_type = models.CharField(max_length=20, choices=CHANGE_TYPE_CHOICES)
    change_quantity = models.IntegerField(help_text="Positive for adding stock, negative for removing.")
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        item = self.product.name if self.product else self.variation
        return f"Log for {item} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"