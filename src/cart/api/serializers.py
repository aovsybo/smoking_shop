from rest_framework import serializers

from cart.models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["cart", "product", "quantity"]


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["product", "quantity"]


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemUpdateSerializer(many=True)

    class Meta:
        model = Cart
        fields = (
            "cart_items",
            "total",
            "status",
        )
