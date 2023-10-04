from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.api.serializers import UserCreateSerializer, UserVerifySerializer
from users.api import verify


class RegisterAPI(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(is_active=True)
        #verify.send(serializer.validated_data['phone'])
        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"]
        )
        login(request, user)

        return Response({
            "message": "successful registration",
            "data": serializer.data,
        }, status=status.HTTP_200_OK)


class VerifyAPI(APIView):
    def post(self, request):
        serializer = UserVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']
        if verify.check(request.user.phone, code):
            request.user.is_verified = True
            request.user.save()
            return Response({
                "message": "verified",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "not verified",
            "data": {"phone": request.user.phone, "code": code}
        }, status=status.HTTP_400_BAD_REQUEST)
