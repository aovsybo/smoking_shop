# Generated by Django 4.2.5 on 2023-10-04 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_producer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name',), 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-date_added',), 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
    ]
