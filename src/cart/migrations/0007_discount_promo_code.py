# Generated by Django 4.2.5 on 2023-10-14 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_discount_cart_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='promo_code',
            field=models.CharField(default='promo', max_length=32, unique=True),
            preserve_default=False,
        ),
    ]
