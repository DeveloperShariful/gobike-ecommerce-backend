# Generated by Django 5.2.4 on 2025-07-28 06:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discounts', '0001_initial'),
        ('orders', '0002_ordertag_order_ip_address_and_more'),
        ('shipping', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='shipping_method',
        ),
        migrations.AddField(
            model_name='order',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='discounts.coupon'),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_rate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shipping.shippingrate'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='tax_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='order',
            name='tracking_url_provider',
            field=models.CharField(blank=True, help_text='URL template for tracking. Use {tracking_number} as a placeholder.', max_length=2000),
        ),
        migrations.AlterField(
            model_name='ordernote',
            name='is_customer_note',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='refund',
            name='restock_items',
            field=models.BooleanField(default=False),
        ),
    ]
