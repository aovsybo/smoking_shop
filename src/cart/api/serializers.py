from rest_framework import serializers

from cart.models import Cart, CartItem, Discount


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity"]


class UsePromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = (
            "promo_code",
        )


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = (
            "status",
        )


class CartsListSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = (
            "user",
            "cart_items",
            "total",
            "discount_total",
            "status",
        )


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = (
            "cart_items",
            "total",
            "discount_total",
            "status",
        )
