from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model

from products.models import Product

User = get_user_model()


class Discount(models.Model):
    discount_percent = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    promo_code = models.CharField(unique=True, max_length=32)
    is_active = models.BooleanField(default=True)


class OrderStatuses(models.TextChoices):
    FILLING = "Filling"
    PROCESSING = "Processing"
    READY = "Ready"
    RECEIVED = "Received"


class Cart(models.Model):
    user = models.ForeignKey(User, related_name="user_cart", on_delete=models.CASCADE)
    discount = models.ForeignKey(Discount, related_name="discount", on_delete=models.CASCADE, default=None, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    discount_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    status = models.CharField(choices=OrderStatuses.choices, default=OrderStatuses.FILLING)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="cart_product", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
