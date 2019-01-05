from django.http import HttpResponse
from .utils import verify_email

# Create your views here.


def activate(request, uidb64, token):
    if verify_email(uidb64, token):
        return HttpResponse('Thank you for your email confirmation.')
    else:
        return HttpResponse('Activation link is invalid!')
