from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend

from products.api.serializers import ProductSerializer, CategorySerializer, CategoryInfoSerializer
from products.models import Product, Category
from products.service import ProductFilter


class ProductsList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter


class ProductCreate(CreateAPIView):
    serializer_class = ProductSerializer


class ProductDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

    def get_object(self):
        try:
            category_slug = self.kwargs["category_slug"]
            product_slug = self.kwargs["product_slug"]
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404


class CategoriesList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryInfoSerializer
    pagination_class = PageNumberPagination


class CategoryDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter

    def get_object(self):
        try:
            category_slug = self.kwargs["category_slug"]
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        category_products = Product.objects.get(category=category.id)
        return Response({
            "message": "verified",
            "products": [category_products]
        }, status=status.HTTP_200_OK)


class CategoryCreate(CreateAPIView):
    serializer_class = CategoryInfoSerializer


class SearchListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("name", "description")
