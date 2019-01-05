from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='registration'),
    path('login/', csrf_exempt(Login.as_view()), name='login'),

]
