from django.urls import path 
from .views import RedistrationView

urlpatterns = {
    path('register', RedistrationView.as_view(), name='register'),   
}