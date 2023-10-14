from drf_yasg import openapi
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView
from drf_yasg.utils import swagger_auto_schema

from users.api.serializers import UserCreateSerializer, UserVerifySerializer, UploadDocumentSerializer
from users.api import verify
from users.models import User


class UploadDocument(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UploadDocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# TODO: add generics
class RegisterAPI(APIView):
    @swagger_auto_schema(request_body=UserCreateSerializer)
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(is_active=True)
        # verify.send(serializer.validated_data['phone'])
        return Response({
            "message": "successful registration",
            "data": serializer.data,
        }, status=status.HTTP_200_OK)


class VerifyAPI(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=UserVerifySerializer,
        manual_parameters=[openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            type=openapi.TYPE_STRING,
        )]
    )
    def post(self, request):
        serializer = UserVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']
        # if verify.check(request.user.phone, code):
        if code == "123456":
            request.user.is_verified = True
            request.user.save()
            return Response({
                "message": "verified",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "not verified",
            "data": {"code": code}
        }, status=status.HTTP_400_BAD_REQUEST)
