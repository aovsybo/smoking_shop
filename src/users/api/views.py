from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView, CreateAPIView

from users.api.serializers import UserCreateSerializer, UserVerifySerializer, UploadDocumentSerializer
from users.api import verify
from users.models import User


class UploadDocument(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UploadDocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class RegisterAPI(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class VerifyAPI(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserVerifySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
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
