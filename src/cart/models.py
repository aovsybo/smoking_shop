from django.db import models
from django.contrib.auth import get_user_model

from products.models import Product

User = get_user_model()


class Cart(models.Model):
    class OrderStatuses(models.TextChoices):
        FILLING = "Filling"
        PROCESSING = "Processing"
        READY = "Ready"
        RECEIVED = "Received"

    user = models.OneToOneField(User, related_name="user_cart", on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    status = models.CharField(choices=OrderStatuses.choices, default=OrderStatuses.FILLING)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="cart_item", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="cart_product", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
