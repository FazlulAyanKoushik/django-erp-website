from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import *

'''
     authentication/
'''

urlpatterns = [
     path('logout', LogoutView.as_view(),
          name='logout'),
     path('login', LoginView.as_view(),
          name='login'),
     path('register', RedistrationView.as_view(),
          name='register'),
     path('validate-username', csrf_exempt(UserNameValidationView.as_view()),
          name='validate-username'),
     path('validate-email', csrf_exempt(EmailValidationView.as_view()),
          name='validate-email'),
     path('validate-pass', csrf_exempt(PasswordCheckerView.as_view()),
          name='validate-pass'),
     path('activate/<uidb64>/<token>', VerificationView.as_view(),
          name='activate'),

     # Reset password
     # path('password-reset', RequestPasswordResetEmailView.as_view(),
     #      name='password-reset'),
]
