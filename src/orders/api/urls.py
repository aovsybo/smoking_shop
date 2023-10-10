from django.urls import path

from orders.api import views

urlpatterns = [
#    path('checkout/', views.checkout),
    path('orders/', views.OrderListCreateView.as_view()),
]
