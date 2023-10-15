# Generated by Django 4.2.5 on 2023-10-14 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_discount_promo_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='discount_total',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]