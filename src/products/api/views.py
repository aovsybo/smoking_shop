from django.db.models import Q
from django.http import Http404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from products.api.serializers import ProductSerializer, CategorySerializer, CreateCategorySerializer
from products.models import Product, Category


class ProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductCreate(APIView):
    @swagger_auto_schema(request_body=ProductSerializer)
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "product created",
            "data": serializer.data,
        }, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response({
            "message": "got product info",
            "data": serializer.data,
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ProductSerializer)
    def put(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(instance=product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "product info updated",
            "data": serializer.data,
        }, status=status.HTTP_200_OK)

    def delete(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        product.delete()
        return Response({
            "message": "product deleted",
            "data": {},
        }, status=status.HTTP_204_NO_CONTENT)


class CategoriesList(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response({
            "message": "got category content",
            "data": serializer.data,
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=CategorySerializer)
    def put(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(instance=category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "category info updated",
            "data": serializer.data,
        }, status=status.HTTP_200_OK)

    def delete(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        category.delete()
        return Response({
            "message": "category deleted",
            "data": {},
        }, status=status.HTTP_204_NO_CONTENT)


class CategoryCreate(APIView):

    @swagger_auto_schema(request_body=CreateCategorySerializer)
    def post(self, request):
        serializer = CreateCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "category created",
            "data": serializer.data,
        }, status=status.HTTP_201_CREATED)


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



