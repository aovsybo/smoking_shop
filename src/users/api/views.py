from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.api.serializers import UserCreateSerializer


class RegisterAPI(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(is_active=True)
        return Response({
            "message": "successful registration",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

