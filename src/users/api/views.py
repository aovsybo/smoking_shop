from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.api.serializers import UserCreateSerializer, LoginSerializer


class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.data)
        if user is None:
            return Response({
                "message": "invalid password",
                "data": {}
            }, status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })


class RegisterAPI(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(is_active=True)
        return Response({
            "message": "successful registration",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

