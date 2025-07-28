# seo/models.py (FINAL VERSION FOR SEO - PHASE 1)

from django.db import models

# ১. রিডাইরেক্ট ম্যানেজমেন্টের জন্য মডেল
class Redirect(models.Model):
    REDIRECT_TYPE_CHOICES = (
        (301, '301 - Permanent Redirect'),
        (302, '302 - Temporary Redirect'),
    )

    source_url = models.CharField(
        max_length=2000, 
        unique=True, 
        help_text="The old URL path. e.g., /old-product-page/"
    )
    target_url = models.CharField(
        max_length=2000, 
        help_text="The new URL path or full URL. e.g., /new-product-page/"
    )
    redirect_type = models.IntegerField(
        choices=REDIRECT_TYPE_CHOICES, 
        default=301
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Redirect"
        verbose_name_plural = "Redirects"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.source_url} -> {self.target_url}"


# ২. গ্লোবাল SEO এবং robots.txt ম্যানেজমেন্টের জন্য মডেল
class GlobalSEOSettings(models.Model):
    # Organization Schema-এর জন্য তথ্য
    organization_name = models.CharField(max_length=255, help_text="Your company or brand name.")
    organization_logo = models.ImageField(upload_to='seo/global/', help_text="Your official logo.")
    organization_url = models.URLField(help_text="Your website's main URL.")
    contact_phone = models.CharField(max_length=20, blank=True, help_text="Your business phone number.")
    contact_email = models.EmailField(blank=True)
    address = models.TextField(blank=True, help_text="Your business address.")

    # robots.txt ফাইলের কন্টেন্ট
    robots_txt_content = models.TextField(
        blank=True,
        default="User-agent: *\nDisallow: /admin/\n\nSitemap: /sitemap.xml",
        help_text="Content for the robots.txt file. Be careful with changes."
    )
    
    class Meta:
        verbose_name = "Global SEO Settings"
        verbose_name_plural = "Global SEO Settings"

    def __str__(self):
        return "Global SEO Settings"

    # একটি মাত্র সেটিংস অবজেক্ট নিশ্চিত করার জন্য
    def save(self, *args, **kwargs):
        self.pk = 1
        super(GlobalSEOSettings, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj