from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser, PermissionsMixin

from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber


class CustomUserManager(BaseUserManager):
    model: 'User'

    def create_user(self, username, phone, password=None, is_staff=False, is_active=True, is_superuser=False):
        normalised_phone = PhoneNumber.from_string(phone_number=phone, region='RU').as_e164
        user = self.model(
            phone=normalised_phone,
            username=username,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
        )
        user.set_password(password)
        user.save()
        return user

    def create_staff(self, username, phone, password=None):
        staff = self.create_user(
            phone,
            username,
            password=password,
            is_staff=True,
        )
        return staff

    def create_superuser(self, username, password=None):
        superuser = self.model(
            phone="",
            username=username,
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        superuser.set_password(password)
        superuser.save()
        return superuser


class User(AbstractUser, PermissionsMixin):
    phone = PhoneNumberField(blank=False, unique=True)
    username = models.CharField(blank=False, unique=True)
    document = models.FileField(upload_to="uploads/documents/")
    document_verified = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class OTP(models.Model):
    code = models.CharField(max_length=8)
