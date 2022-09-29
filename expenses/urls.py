from django.urls import path
from . import views

'''
expenses
'''

urlpatterns = [
    path('', views.index, name='expenses'),
    path('add-expenses/', views.add_expense, name='add-expenses'),
]