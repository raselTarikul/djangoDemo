from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.


class User(AbstractUser):
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Company(models.Model):
    name = models.CharField(max_length=200)
    email_address = models.CharField(max_length=254)
    address = models.TextField()
    phone_number = models.CharField(max_length=200)
    favourite = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='user_favourite')

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name

