from django.urls import path
from .views import *



urlpatterns = [
    path('register/', UserRegistration.as_view(), name='registration'),
    path('login/', Login.as_view(), name='login'),
    path('change_password/', ChangePassword.as_view(), name='change_password'),
    path('companies/', CompanyList.as_view(), name='company_list'),
    path('companies/favourite/', FavouriteCompanyList.as_view(), name='company_list'),
    path('make_favourite/<int:company_id>/', MakeFavourite.as_view(), name='make_favourite'),
    path('un_favourite/<int:company_id>/', UnFavourite.as_view(), name='un_favourite'),

]
