from rest_framework import serializers

from users.models import User, OTP


class UploadDocumentSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['document']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta(object):
        model = User
        fields = ['id', 'username', 'phone', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserVerifySerializer(serializers.ModelSerializer):
    class Meta(object):
        model = OTP
        fields = ['code']
