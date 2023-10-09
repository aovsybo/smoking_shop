from django.db.models import Q
from django.http import Http404

from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from products.api.serializers import ProductSerializer, CategorySerializer, CreateCategorySerializer
from products.models import Product, Category


class ProductsList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductCreate(CreateAPIView):
    serializer_class = ProductSerializer


class ProductDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer

    def get_object(self):
        try:
            category_slug = self.kwargs["category_slug"]
            product_slug = self.kwargs["product_slug"]
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404


class CategoriesList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer

    def get_object(self):
        try:
            category_slug = self.kwargs["category_slug"]
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404


class CategoryCreate(CreateAPIView):
    serializer_class = CreateCategorySerializer


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'query': openapi.Schema(type=openapi.TYPE_STRING, description='query')
    }),
                     responses={200: ProductSerializer, 400: 'Bad Request'})
@api_view(["POST"])
def search(request):
    query = request.data.get('query', '')
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({"products": []})
