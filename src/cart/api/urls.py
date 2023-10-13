from django.urls import path

from cart.api import views

urlpatterns = [
    path("cart/add/", views.CartItemAPIView.as_view()),
    path("cart/createOrder/", views.CreateOrder.as_view()),
    path("cart/", views.CartView.as_view()),
    path("cart/history/", views.OrdersList.as_view()),
    path("cart/item/<int:pk>/", views.CartItemView.as_view()),
]
