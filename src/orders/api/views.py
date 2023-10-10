from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
import stripe

from orders.models import Order, OrderItem
from orders.api.serializers import OrderSerializer, OrderItemSerializer
from products.models import Product
from cart.models import CartItem


class OrderListCreateView(ListCreateAPIView):
    def get_queryset(self):
        user = self.request.user
        queryset = CartItem.objects.filter(cart__user=user)
        return queryset
    serializer_class = OrderItemSerializer

    # def create(self, request, *args, **kwargs):
    #     order = Order.objects.filter(user=request.user)
    #     if not order:
    #         order = Order().create_order(request.user, True)

#
# class OrderView(ListCreateAPIView):
#     serializer_class = OrderItemSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         queryset = Order.objects.filter(user=user)
#         return queryset
#
#     def create(self, request, *args, **kwargs):
#         user = request.user
#         product = get_object_or_404(Product, pk=request.data["product"])
#         quantity = request.data.get("quantity", 1)
#         order = self.get_queryset()
#         if not order:
#             order = Order().create_order(user, True)
#         price = quantity * product.price
#         order_item = OrderItem().create_order_item(order, product, quantity, price)
#         serializer = OrderItemSerializer(order_item)
#         # TODO Payment Integration here.
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
