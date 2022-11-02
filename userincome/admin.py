from django.contrib import admin
from .models import *

# Register your models here.
class UserIncomeAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'date', 'source', 'description',)
    search_fields = ('user', 'amount', 'date', 'source', 'description',)
    list_per_page = 5

admin.site.register(UserIncome, UserIncomeAdmin)

class SourceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
admin.site.register(Source, SourceAdmin)