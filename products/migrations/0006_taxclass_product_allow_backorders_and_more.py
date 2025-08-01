# Generated by Django 5.2.4 on 2025-07-28 06:49

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_inventorylog_order_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaxClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='e.g., Standard Rate, Zero Rate', max_length=100, unique=True)),
                ('rate_percentage', models.DecimalField(decimal_places=2, default=0.0, help_text='Tax rate in percentage. e.g., 15 for 15%.', max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
            ],
            options={
                'verbose_name': 'Tax Class',
                'verbose_name_plural': 'Tax Classes',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='allow_backorders',
            field=models.CharField(choices=[('no', 'Do not allow'), ('notify', 'Allow, but notify customer'), ('yes', 'Allow')], default='no', max_length=10),
        ),
        migrations.AddField(
            model_name='productvariation',
            name='allow_backorders',
            field=models.CharField(choices=[('no', 'Do not allow'), ('notify', 'Allow, but notify customer'), ('yes', 'Allow')], default='no', max_length=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock_quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='productvariation',
            name='stock_quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='tax_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.taxclass'),
        ),
    ]
