import decimal

from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from .serializers import CartItemSerializer, CartItemUpdateSerializer, CartSerializer
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied

from cart.models import Cart, CartItem
from products.models import Product


class CartView(ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    pagination_class = None

    def get_object(self):
        try:
            user = self.kwargs["user"]
            return Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            raise Http404


class CartItemAPIView(CreateAPIView):
    serializer_class = CartItemUpdateSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = CartItem.objects.filter(cart__user=user)
        return queryset

    def create(self, request, *args, **kwargs):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        # cart = get_object_or_404(Cart, user=user)
        product = get_object_or_404(Product, pk=request.data["product"])
        quantity = int(request.data["quantity"])
        existing_cart_item = CartItem.objects.filter(product=product, cart=cart).first()
        if existing_cart_item:
            # If it exists, increase the quantity
            existing_cart_item.quantity += quantity
            existing_cart_item.save()
            serializer = CartItemUpdateSerializer(existing_cart_item, data=request.data)
        else:
            # If it doesn't exist, create a new CartItem
            cart_item = CartItem(product=product, quantity=quantity, cart=cart)
            cart_item.save()
            serializer = CartItemUpdateSerializer(cart_item, data=request.data)
        cart.total += decimal.Decimal(float(product.price) * float(quantity))
        cart.save()
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartItemView(RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemUpdateSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = CartItem.objects.filter(cart__user=user)
        return queryset
