from django.urls import path

from products.api import views

urlpatterns = [
    path('products/all/', views.ProductsList.as_view()),
    path('products/categories/', views.CategoriesList.as_view()),
    path('products/search/', views.search),
    path('products/create_product/', views.ProductCreate.as_view()),
    path('products/create_category/', views.CategoryCreate.as_view()),
    path('products/<slug:category_slug>/', views.CategoryDetail.as_view()),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
]
