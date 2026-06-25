from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin


@admin.register(models.CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('id',)


admin.register(models.EmailConfirm)
class EmailConfirmAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'code')