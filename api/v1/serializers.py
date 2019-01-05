from rest_framework import serializers
from django.conf import settings
from app.models import User, Company


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer class for User Registration,
    """

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class LogInSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class ChangePassSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    new_password = serializers.CharField(max_length=255)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name', 'email_address', 'address', 'phone_number')


