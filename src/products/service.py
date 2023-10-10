from django_filters import rest_framework as filters

from products.models import Product


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class ProductFilter(filters.FilterSet):
    price = filters.NumberFilter()
    price__gt = filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = filters.NumberFilter(field_name='price', lookup_expr='lt')
    producer = CharFilterInFilter(field_name='producer', lookup_expr='in')
    category = CharFilterInFilter(field_name='category__name', lookup_expr='in')

    class Meta:
        model = Product
        fields = ['price', 'producer', 'category']
