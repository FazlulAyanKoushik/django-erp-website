from django.urls import path
from . import views

'''
    preferences
'''

urlpatterns = [
    path('', views.index, name='preferences'),
]