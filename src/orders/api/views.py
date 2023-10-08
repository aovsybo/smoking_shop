from django.conf import settings
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
import stripe

from orders.models import Order, OrderItem
from orders.api.serializers import OrderSerializer
from users.models import User


@api_view(['POST'])
# @authentication_classes([authentication.TokenAuthentication])
# @permission_classes([permissions.IsAuthenticated])
def checkout(request):
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    paid_amount = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])
    try:
        charge = stripe.Charge.create(
            amount=int(paid_amount * 100),
            currency='USD',
            description='Charge from Djackets',
            source=serializer.validated_data['stripe_token']
        )
        serializer.save(user=request.user, paid_amount=paid_amount)
        return Response({
            "message": "order created",
            "data": serializer.data,
        }, status=status.HTTP_201_CREATED)
    except Exception:
        return Response({
            "message": "bad request",
            "data": {},
        }, status=status.HTTP_400_BAD_REQUEST)
