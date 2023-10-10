from rest_framework import serializers

from orders.models import OrderItem, Order
from products.api.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(required=False, read_only=True)

    class Meta:
        model = OrderItem
        exclude = ('order',)
