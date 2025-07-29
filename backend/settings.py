# backend/settings.py (FINAL VERSION - UPDATED FOR API KEYS & EMAIL)

from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-your-secret-key'
DEBUG = True

ALLOWED_HOSTS = ['gobike-ecommerce-backend.onrender.com', 'localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    # Third-party apps
    'rest_framework',
    'corsheaders',
    'ckeditor',
    'import_export',
    'django_countries',

    # Local apps
    'analytics', 'customers', 'discounts', 'orders',
    'payments', 'products', 'seo', 'shipping', 'site_settings',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'site_settings.context_processors.global_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static & Media files
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

if not DEBUG:
    STORAGES = {
        "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
    }

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS Headers Settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",        # Django admin and traditional pages
    "http://127.0.0.1:8000",
    "http://localhost:3000",        # Future Next.js frontend
    "http://127.0.0.1:3000",
    "https://gobike-ecommerce-backend.onrender.com", # Your live Render backend
    # "https://your-frontend-domain.com", # Future Next.js live domain
]
# Session ID for the shopping cart
CART_SESSION_ID = 'cart'

# Jazzmin UI Configuration
# backend/settings.py (শুধুমাত্র JAZZMIN_SETTINGS আপডেট করুন)

JAZZMIN_SETTINGS = {
    # --- General ---
    "site_title": "GoBike Admin",
    "site_header": "GoBike",
    "site_brand": "GoBike Dashboard",
    "welcome_sign": "Welcome to the GoBike Admin Panel",
    "copyright": "GoBike Ltd.",
    
    # --- Search ---
    "search_model": ["products.Product", "orders.Order", "auth.User"],

    # --- Top Menu ---
    "topmenu_links": [
        {"name": "Home", "url": "admin:index"},
        {"name": "View Site", "url": "/", "new_window": True},
        {"model": "products.Product"},
    ],

    # --- UI ---
    "show_sidebar": True,
    "navigation_expanded": True,
    "changeform_format": "horizontal_tabs",
    "related_modal_active": True,
    "custom_css": None,
    "custom_js": None,

    # --- Icons ---
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "products": "fas fa-shopping-cart",
        "products.Product": "fas fa-bicycle",
        "products.Category": "fas fa-tags",
        "orders": "fas fa-file-invoice-dollar",
        "orders.Order": "fas fa-file-invoice",
        "seo": "fas fa-chart-line",
        "shipping": "fas fa-shipping-fast",
        "discounts": "fas fa-percent",
        "payments": "fas fa-credit-card",
        "customers": "fas fa-users",
        "site_settings": "fas fa-cogs",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    # --- নতুন: Import-Export এবং অন্যান্য ফিচারের জন্য ইন্টিগ্রেশন ---
    "language_chooser": False, # Hides the language chooser dropdown

    # এটি import-export বাটনগুলোকে ফিরিয়ে আনবে
    "changeform_format_overrides": {
        "products.Product": "collapsible",
        "orders.Order": "collapsible",
    },

    # এটি Django-এর ডিফল্ট অ্যাকশনগুলোকে (যেমন Duplicate Product) আরও সুন্দরভাবে দেখাবে
    # এবং django-admin-actions-এর সাথে সামঞ্জস্যপূর্ণ
    "actions_sticky_top": True,
}

# --- নতুন: External API Keys ---
# গুরুত্বপূর্ণ: প্রোডাকশনে এগুলো এনভায়রনমেন্ট ভেরিয়েবল থেকে লোড করা উচিত!
# os.environ.get('STRIPE_PUBLISHABLE_KEY')
STRIPE_PUBLISHABLE_KEY = 'your_stripe_publishable_key'  # <-- আপনার Stripe Publishable Key এখানে দিন
STRIPE_SECRET_KEY = 'your_stripe_secret_key'          # <-- আপনার Stripe Secret Key এখানে দিন

TRANSDIRECT_API_KEY = '47252f94501e01fdfbec79e95f830203'      # <-- আপনার Transdirect API Key এখানে দিন

# --- নতুন: Email Backend for Development ---
# ইমেইল পাঠানোর বদলে কনসোলে দেখানোর জন্য
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# --- Site ID (সাইটম্যাপ ফ্রেমওয়ার্কের জন্য দরকার হতে পারে) ---
SITE_ID = 1