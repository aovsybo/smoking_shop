import decimal

from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from .serializers import CartItemUpdateSerializer, CartSerializer
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q

from cart.models import Cart, CartItem
from products.models import Product


class OrdersList(ListAPIView):
    queryset = Cart.objects.filter(~Q(status="Filling"))
    serializer_class = CartSerializer

    def get_object(self):
        try:
            user = self.kwargs["user"]
            return Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            raise Http404


class CartView(ListAPIView):
    queryset = Cart.objects.filter(status="Filling")
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
        queryset = CartItem.objects.filter(cart__user=user, cart__status="Filling")
        return queryset

    def create(self, request, *args, **kwargs):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user, status="Filling")
        product = get_object_or_404(Product, pk=request.data["product"])
        quantity = int(request.data["quantity"])
        cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)
        data = {"quantity": quantity, "product": product.pk}
        if not created:
            data["quantity"] += cart_item.quantity
        cart_item.save()
        serializer = CartItemUpdateSerializer(cart_item, data=data)
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

    def update(self, request, *args, **kwargs):
        cart_item = self.get_object()
        product = get_object_or_404(Product, pk=request.data["product"]) \
            if "product" in request.data.keys() \
            else cart_item.product
        quantity = int(request.data["quantity"]) \
            if request.data["quantity"] \
            else cart_item.quantity
        data = {"product": product.pk, "quantity": quantity}
        cart = cart_item.cart
        cart.total += decimal.Decimal(float(product.price) * float(cart_item.quantity - quantity))
        cart.save()
        serializer = self.serializer_class(cart_item, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        cart_item = self.get_object()
        cart = cart_item.cart
        cart.total -= decimal.Decimal(float(cart_item.product.price) * float(cart_item.quantity))
        cart.save()
        cart_item.delete()
        return Response(
            {"message": "deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )
