# Generated by Django 4.2.5 on 2023-10-12 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_cart_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='status',
            field=models.CharField(choices=[('Filling', 'Filling'), ('Processing', 'Processing'), ('Ready', 'Ready'), ('Received', 'Received')], default='Filling'),
        ),
    ]
