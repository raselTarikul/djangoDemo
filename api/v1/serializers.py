from rest_framework import serializers
from django.conf import settings
from app.exceptions import UserAlreadyExistExceptions
from app.models import User, Company


class UserRegistrationSerializer(serializers.Serializer):
    """
    Serializer class for User Registration,
    """

    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, required=True)

    def create(self, validated_data):
        username = validated_data.get('username', None)
        email = validated_data.get('email', None)
        password = validated_data.get('password', None)

        user, created = User.objects.get_or_create(username=username)
        if not created:
            raise UserAlreadyExistExceptions("User already exists with this username.")
        else:
            user.set_password(password)
            user.email = email
            user.save()
            return user


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
        fields = ('id', 'name', 'address', 'phone_number')


