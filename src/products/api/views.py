from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from products.api.serializers import (
    ProductSerializer,
    ProductCreateSerializer,
    CategorySerializer,
    CategoryInfoSerializer,
    )
from products.models import Product, Category
from products.service import ProductFilter
from products.permissions import IsAdminOrSafeMethods
from products.parse_data import parse_products_info
from config.services import CustomPagination


class ProductsList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter


class ProductCreate(CreateAPIView):
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAdminUser]


class ProductDetailById(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrSafeMethods]

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Product.objects.filter(pk=pk)


class ProductDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
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
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly]


class CategoryDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
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
    pagination_class = CustomPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("name", "description")
    permission_classes = [IsAuthenticatedOrReadOnly]


class ParseCatalog(APIView):
    def post(self, request, *args, **kwargs):
        products = parse_products_info()
        categories = self.get_categories_from_products(products)
        response_data = self.create_categories(categories)
        return Response(response_data, status=status.HTTP_201_CREATED)

    def create_categories(self, categories):
        created_objects = []
        errors = []
        for category in categories:
            if Category.objects.filter(name=category).count() == 0:
                data = {
                    "name": category,
                    "slug": self.get_slug_from_str(category),
                }
                serializer = CategoryInfoSerializer(data=data)
                if serializer.is_valid():
                    created_objects.append(serializer.save())
                else:
                    errors.append(serializer.errors)
        response_data = {
            'created_objects': CategorySerializer(created_objects, many=True).data,
            'errors': errors,
        }
        return response_data

    @staticmethod
    def get_categories_from_products(products):
        return list(set([product['category'] for product in products]))

    @staticmethod
    def get_slug_from_str(name: str):
        return "".join(
            [letter for letter in name if letter.isalpha() or letter.isdigit() or letter == ' ']
        ).replace(' ', '-').replace('--', '-')[:50]
