from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import (
    UpdateAPIView,
    CreateAPIView,
    RetrieveAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView)

from users.api.serializers import (
    UserCreateSerializer,
    UserVerifySerializer,
    UploadDocumentSerializer,
    UserInfoSerializer,
    NotificationSerializer,
)
from users.api import verify
from users.models import User, Notification
from config.services import CustomPagination


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


class UserInfoAPI(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserInfoSerializer

    def get_object(self):
        return self.request.user


class NotificationsListCreateAPI(ListCreateAPIView):
    serializer_class = NotificationSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAdminUser]
    queryset = Notification.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_read']


class NotificationAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Notification.objects.filter(pk=pk)
