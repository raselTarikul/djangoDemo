from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.


class User(AbstractUser):
    """
    Users represented by this
    model.

    Username, email and password are required. Other fields are optional.
    """
    is_verified = models.BooleanField(_('verification status'), default=False)
    email = models.EmailField(_('email address'))

    def __str__(self):
        return self.username


class Company(models.Model):
    """
    Company model is represented by this Class

    Name, Email address and Phone field is required
    """
    name = models.CharField(_('email address'), max_length=200)
    email_address = models.EmailField(_('email address'))
    address = models.TextField(_('address'))
    phone_number = models.CharField(_('email address'), max_length=200)
    favourite = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='user_favourite')

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name

