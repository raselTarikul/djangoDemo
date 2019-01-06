from django.db import models
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from app.exceptions import UserAlreadyExistExceptions
from app.models import User, Company
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework import filters
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
            try:
                user = serializer.save()
                send_verification_email(user, request)
                return Response({'message': 'Your registration completed.'}, status=status.HTTP_201_CREATED)
            except UserAlreadyExistExceptions:
                return Response({'message': 'User already exists with this username'}, status.HTTP_406_NOT_ACCEPTABLE)

        else:
            return Response(serializer.errors, status.HTTP_406_NOT_ACCEPTABLE)


class Login(APIView):
    """
    Login isn api view
    """
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
                if user.check_password(password):
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({
                        'token': token.key,
                    }, status=200)
                else:
                    return Response({'message': 'Invalid Password'}, status.HTTP_406_NOT_ACCEPTABLE)
            except models.ObjectDoesNotExist:
                return Response({'message': 'User does not exists'}, status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(serializer.errors, status.HTTP_406_NOT_ACCEPTABLE)


class ChangePassword(APIView):
    """
    Change password api view
    """
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


class CompanyList(ListAPIView):
    """
    Company list api views
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class FavouriteCompanyList(ListAPIView):
    """
    Users favorait api views
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_queryset(self):
        return self.request.user.user_favourite.all()


class MakeFavourite(APIView):
    """
    Api view for user to make favorate company
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        pk = kwargs['company_id'] if 'company_id' in kwargs.keys() else None
        if pk:
            try:
                user = request.user
                company = Company.objects.get(id=pk)
                user.user_favourite.add(company)
                return Response({'message': 'success'}, status=status.HTTP_202_ACCEPTED)
            except models.ObjectDoesNotExist:
                return Response({'message': 'Company not exists'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({'message': 'Company id is not provided'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class UnFavourite(APIView):
    """
    Api view for user to make favorate company
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        pk = kwargs['company_id'] if 'company_id' in kwargs.keys() else None
        if pk:
            try:
                user = request.user
                company = Company.objects.get(id=pk)
                user.user_favourite.remove(company)
                return Response({'message': 'success'}, status=status.HTTP_202_ACCEPTED)
            except models.ObjectDoesNotExist:
                return Response({'message': 'Company not exists'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({'message': 'Company id is not provided'}, status=status.HTTP_406_NOT_ACCEPTABLE)
