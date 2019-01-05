from django.db import models
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import User, Company
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from api.v1 import schema
from .serializers import UserRegistrationSerializer, LogInSerializer, ChangePassSerializer, CompanySerializer
from app.utils import send_verification_email


class UserRegistration(APIView):
    """
    User Registration API
    """
    schema = schema.registration_schema

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_verification_email(user, request)
            return Response({'message': 'Your registration completed.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_406_NOT_ACCEPTABLE)


class Login(APIView):
    schema = schema.login_schema

    def post(self, request):
        serializer = LogInSerializer(data=request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(username=username)
                if not user.is_verified:
                    return Response({'message': 'User not verified'}, status.HTTP_406_NOT_ACCEPTABLE)
                if check_password(password, user.password):
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({
                        'token': token.key,
                    }, status=200)
                else:
                    return Response({'message': 'Invalid Password'}, status.HTTP_406_NOT_ACCEPTABLE)
            except User.DoesNotExist:
                return Response({'message': 'User does not exists'}, status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(serializer.errors, status.HTTP_406_NOT_ACCEPTABLE)


class ChangePassword(APIView):
    schema = schema.change_pass_schema
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = ChangePassSerializer(data=request.data,
                                          context={'request': request})
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            new_password = serializer.validated_data['new_password']
            try:
                user = User.objects.get(username=username)
                if check_password(password, user.password):
                    user.set_password(new_password)
                    user.save()
                    return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Invalid Password'}, status.HTTP_406_NOT_ACCEPTABLE)
            except User.DoesNotExist:
                return Response({'message': 'User does not exists'}, status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({'message': 'Field Validation Error'}, status.HTTP_406_NOT_ACCEPTABLE)


class CompanyList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        companies = Company.objects.all()
        serializers = CompanySerializer(companies, many=True)
        return Response(serializers.data)


class FavouriteCompanyList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        companies = request.user.user_favourite
        serializers = CompanySerializer(companies, many=True)
        return Response(serializers.data)


class MakeFavourite(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        pk = kwargs['company_id'] if 'company_id' in kwargs.keys() else None
        if pk:
            try:
                user = request.user
                company = Company.objects.get(category=pk)
                user.user_favourite.add(company)
                user.save()
            except models.ObjectDoesNotExist:
                return Response({'message': 'Company not exists'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({'message': 'Company id is not provided'}, status=status.HTTP_406_NOT_ACCEPTABLE)


