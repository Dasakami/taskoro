from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile, CharacterClass, Medal, CustomGroup, CustomPermission


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """Админка для кастомного пользователя"""
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ()}),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'level', 'experience', 'coins', 'gems', 'streak']
    search_fields = ['user__username', 'user__email']
    list_filter = ['level', 'theme_preference']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CharacterClass)
class CharacterClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'color']
    search_fields = ['name']


@admin.register(Medal)
class MedalAdmin(admin.ModelAdmin):
    list_display = ['name', 'profile', 'medal_type', 'acquired_date']
    list_filter = ['medal_type', 'acquired_date']
    search_fields = ['name', 'profile__user__username']


@admin.register(CustomGroup)
class CustomGroupAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(CustomPermission)
class CustomPermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'codename']
    search_fields = ['name', 'codename']