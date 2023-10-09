from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.api import views

urlpatterns = [
    path('account/register/', views.RegisterAPI.as_view()),
    path('account/verify/', views.VerifyAPI.as_view()),
    path('account/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('account/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
