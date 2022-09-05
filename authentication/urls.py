from django.urls import path 
from django.views.decorators.csrf import csrf_exempt
from .views import *
urlpatterns = {
    path('register', RedistrationView.as_view(), name='register'),   
    path('validate-username', csrf_exempt(UserNameValidationView.as_view()), name='validate-username'),   
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name='validate-email'),   
}