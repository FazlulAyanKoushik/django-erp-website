from django.contrib import admin
from .models import UserPreference

# Register your models here.
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'currency',)


admin.site.register(UserPreference, UserPreferenceAdmin)