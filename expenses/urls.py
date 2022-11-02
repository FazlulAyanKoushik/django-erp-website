from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from .views import *
'''
expenses
'''

urlpatterns = [
    path('', views.index, name='expenses'),
    path('search-expenses/', csrf_exempt(views.search_expenses), name='search-expenses'),
    path('add-expense/', views.add_expense, name='add-expense'),
    path('edit-expense/<int:id>', views.edit_expense, name='edit-expense'),
    path('delete-expense/<int:id>', views.delete_expense, name='delete-expense'),
    
    path('expense-category-summary', views.expence_cateogry_summery, name='expense-category-summary'),
    path('stats', views.stats, name='stats'),
    path('export-csv', views.export_csv, name='export-csv'),
    path('export-excel', views.export_excel, name='export-excel'),
    # path('export-pdf', views.export_pdf, name='export-pdf'),
    path('export-pdf', ExportPdfView.as_view(),name='export-pdf'),
]