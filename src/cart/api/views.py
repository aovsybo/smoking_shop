import decimal

from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    ListCreateAPIView
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q

from cart.api.serializers import (
    CartItemSerializer,
    CartSerializer,
    CreateOrderSerializer,
    CartsListSerializer,
    DiscountSerializer,
    UsePromoSerializer,
)
from cart.models import Cart, CartItem, OrderStatuses, Discount
from cart.permissions import IsVerified
from products.models import Product
from config.services import CustomPagination


class UsePromoAPIView(UpdateAPIView):
    serializer_class = UsePromoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            promo_code = self.request.data["promo_code"]
            return Discount.objects.get(promo_code=promo_code)
        except Discount.DoesNotExist:
            raise Http404

    def update(self, request, *args, **kwargs):
        cart = Cart.objects.get(status="Filling", user=request.user)
        discount = self.get_queryset()
        if discount and discount.is_active:
            cart.discount = discount
            discount_part = 1 - cart.discount.discount_percent / 100
            discount_price = round(float(cart.total) * float(discount_part), 2)
            cart.discount_total = decimal.Decimal(discount_price)
            cart.save()
            return Response(status=status.HTTP_200_OK)
        return Response({"message": "Promo does not exists"}, status=status.HTTP_400_BAD_REQUEST)


class DiscountCreateListAPIView(ListCreateAPIView):
    serializer_class = DiscountSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAdminUser]
    queryset = Discount.objects.all()


class DiscountAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DiscountSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Discount.objects.filter(pk=pk)


class CreateOrder(UpdateAPIView):
    serializer_class = CreateOrderSerializer
    permission_classes = [IsAuthenticated, IsVerified]
    queryset = Cart.objects.filter(status="Filling")

    def get_object(self):
        try:
            user = self.request.user
            return Cart.objects.get(status="Filling", user=user)
        except Cart.DoesNotExist:
            raise Http404

    def update(self, request, *args, **kwargs):
        cart = self.get_object()
        cart.status = OrderStatuses.PROCESSING
        cart.save()
        return Response(status=status.HTTP_200_OK)


class OrdersList(ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        try:
            user = self.request.user
            return Cart.objects.filter(~Q(status="Filling"), user=user)
        except Cart.DoesNotExist:
            raise Http404


class AllCartsView(ListAPIView):
    serializer_class = CartsListSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination
    queryset = Cart.objects.all()


class CartView(ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        try:
            user = self.request.user
            return Cart.objects.filter(status="Filling", user=user)
        except Cart.DoesNotExist:
            raise Http404


class CartItemAPIView(CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

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
        serializer = self.serializer_class(cart_item, data=data)
        sum_price = float(product.price) * float(quantity)
        cart.total += decimal.Decimal(sum_price)
        if cart.discount:
            discount_part = 1 - cart.discount.discount_percent / 100
            discount_price = round(sum_price * float(discount_part), 2)
            cart.discount_total += decimal.Decimal(discount_price)
        else:
            cart.discount_total += decimal.Decimal(sum_price)
        cart.save()
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartItemView(RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

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
        sum_price = float(product.price) * float(quantity - cart_item.quantity)
        cart.total += decimal.Decimal(sum_price)
        if cart.discount:
            discount_part = 1 - cart.discount.discount_percent / 100
            discount_price = round(sum_price * float(discount_part), 2)
            cart.discount_total += decimal.Decimal(discount_price)
        else:
            cart.discount_total += decimal.Decimal(sum_price)
        cart.save()
        serializer = self.serializer_class(cart_item, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        cart_item = self.get_object()
        cart = cart_item.cart
        sum_price = float(cart_item.product.price) * float(cart_item.quantity)
        cart.total -= decimal.Decimal(sum_price)
        if cart.discount:
            discount_part = 1 - cart.discount.discount_percent / 100
            discount_price = round(sum_price * float(discount_part), 2)
            cart.discount_total -= decimal.Decimal(discount_price)
        else:
            cart.discount_total -= decimal.Decimal(sum_price)
        cart.save()
        cart_item.delete()
        return Response(
            {"message": "deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )
