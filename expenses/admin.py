from django.contrib import admin
from .models import Expense, Category


# Register your models here.
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'date', 'category', 'description',)
    search_fields = ('amount', 'date', 'category', 'description',)
    list_per_page = 5


admin.site.register(Expense, ExpenseAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)


admin.site.register(Category, CategoryAdmin)
