from django.urls import path 
from django.views.decorators.csrf import csrf_exempt
from .views import RedistrationView, UserNameValidationView

urlpatterns = {
    path('register', RedistrationView.as_view(), name='register'),   
    path('validate-username', 
         csrf_exempt(UserNameValidationView.as_view()), 
         name='validate-username'),   
}