from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, BasePermission
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend

from products.api.serializers import (
    ProductSerializer,
    ProductCreateSerializer,
    CategorySerializer,
    CategoryInfoSerializer,
    )
from products.models import Product, Category
from products.service import ProductFilter

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class IsAdminOrSafeMethods(BasePermission):
    """
    The request is authenticated as an admin, or method is safe.
    """
    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS or
                request.user and
                request.user.is_staff):
            return True
        return False


class ProductsList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter


class ProductCreate(CreateAPIView):
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAdminUser]


class ProductDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrSafeMethods]

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
    permission_classes = [IsAuthenticatedOrReadOnly]


class CategoryDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    permission_classes = [IsAdminOrSafeMethods]

    def get_object(self):
        try:
            category_slug = self.kwargs["category_slug"]
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        return Response({
            'products': self.serializer_class(category).data["products"],
        })


class CategoryCreate(CreateAPIView):
    serializer_class = CategoryInfoSerializer
    permission_classes = [IsAdminUser]


class SearchListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("name", "description")
    permission_classes = [IsAuthenticatedOrReadOnly]
