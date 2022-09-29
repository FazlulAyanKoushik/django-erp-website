from django.contrib import admin
from .models import Expense, Category


# Register your models here.
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'date', 'category', 'description',)


admin.site.register(Expense, ExpenseAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)


admin.site.register(Category, CategoryAdmin)
