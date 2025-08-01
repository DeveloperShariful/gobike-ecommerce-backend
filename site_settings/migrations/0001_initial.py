# Generated by Django 5.2.4 on 2025-07-28 06:49

import django_countries.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StoreSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(default='GoBike', max_length=100)),
                ('store_slogan', models.CharField(blank=True, max_length=255)),
                ('store_logo', models.ImageField(blank=True, null=True, upload_to='settings/logo/')),
                ('address_line_1', models.CharField(max_length=255)),
                ('address_line_2', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=20)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('support_email', models.EmailField(help_text='Email for customer support.', max_length=254)),
                ('support_phone', models.CharField(blank=True, max_length=20)),
                ('currency', models.CharField(choices=[('USD', 'US Dollar ($)'), ('EUR', 'Euro (€)'), ('GBP', 'British Pound (£)'), ('BDT', 'Bangladeshi Taka (৳)'), ('AUD', 'Australian Dollar (A$)')], default='USD', max_length=3)),
                ('weight_unit', models.CharField(choices=[('kg', 'Kilogram (kg)'), ('g', 'Gram (g)'), ('lbs', 'Pound (lbs)'), ('oz', 'Ounce (oz)')], default='kg', max_length=3)),
                ('dimension_unit', models.CharField(choices=[('m', 'Meter (m)'), ('cm', 'Centimeter (cm)'), ('mm', 'Millimeter (mm)'), ('in', 'Inch (in)'), ('yd', 'Yard (yd)')], default='cm', max_length=2)),
                ('google_analytics_id', models.CharField(blank=True, help_text='Your Google Analytics Tracking ID (e.g., UA-12345678-1 or G-XXXXXXXXXX).', max_length=50)),
                ('facebook_pixel_id', models.CharField(blank=True, help_text='Your Facebook Pixel ID.', max_length=50)),
            ],
            options={
                'verbose_name': 'Store Settings',
                'verbose_name_plural': 'Store Settings',
            },
        ),
    ]
