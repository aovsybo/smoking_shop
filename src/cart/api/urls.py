from django.urls import path

from cart.api import views

urlpatterns = [
    path("cart/", views.CartView.as_view()),
    path("cart/all/", views.AllCartsView.as_view()),
    path("cart/add/", views.CartItemAPIView.as_view()),
    path("cart/use_promo/", views.UsePromoAPIView.as_view()),
    path("cart/createOrder/", views.CreateOrder.as_view()),
    path("cart/history/", views.OrdersList.as_view()),
    path("cart/item/<int:pk>/", views.CartItemView.as_view()),
    path("discounts/", views.DiscountCreateListAPIView.as_view()),
    path("discounts/<int:pk>/", views.DiscountAPIView.as_view()),
]
