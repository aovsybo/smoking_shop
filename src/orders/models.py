from django.db import models

from users.models import User
from products.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

# class Order(models.Model):
#     class OrderStatuses(models.TextChoices):
#         PROCESSING = "Processing"
#         READY = "Ready"
#         RECEIVED = "Received"
#
#     user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
#     status = models.CharField(choices=OrderStatuses.choices, default=OrderStatuses.PROCESSING)
#     created_at = models.DateTimeField(auto_now_add=True)
#     total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
#     is_paid = models.BooleanField(default=False)
#
#     class Meta:
#         ordering = ['-created_at', ]
#
#     @staticmethod
#     def create_order(user, is_paid=False):
#         order = Order()
#         order.user = user
#         order.is_paid = is_paid
#         order.save()
#         return order
#
#
# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, related_name='item_order', on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, related_name='product_order', on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     price = models.DecimalField(max_digits=8, decimal_places=2)
#
#     @staticmethod
#     def create_order_item(order, product, quantity, price):
#         order_item = OrderItem()
#         order_item.order = order
#         order_item.product = product
#         order_item.quantity = quantity
#         order_item.price = price
#         order_item.save()
#         return order_item

