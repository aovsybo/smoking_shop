# from django.db import models
#
# from users.models import User
# from products.models import Product
#
#
# class Order(models.Model):
#     class OrderStatuses(models.TextChoices):
#         PROCESSING = "Processing"
#         READY = "Ready"
#         RECEIVED = "Received"
#
#     user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
#     status = models.CharField(choices=OrderStatuses.choices, default=OrderStatuses.PROCESSING)
#     created_at = models.DateTimeField(auto_now_add=True)
#     paid_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
#     stripe_token = models.CharField(max_length=100)
#
#     class Meta:
#         ordering = ['-created_at', ]
#
#
# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=8, decimal_places=2)
#     quantity = models.IntegerField(default=1)
#
#     def __str__(self):
#         return '%s' % self.id
#
