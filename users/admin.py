from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

from django.contrib import admin
from .models import Medal

@admin.register(Medal)
class MedalAdmin(admin.ModelAdmin):
    list_display = ('name', 'profile', 'medal_type', 'acquired_date')
    search_fields = ('name', 'profile__user__username')

