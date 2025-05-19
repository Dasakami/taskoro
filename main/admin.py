from django.contrib import admin
from .models import DailyMission, DailyMotivation

@admin.register(DailyMission)
class DailyMissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'experience_reward', 'assigned_to', 'date_created', 'date_completed')
    list_filter = ('date_created', 'date_completed')
    search_fields = ('title', 'description')

@admin.register(DailyMotivation)
class DailyMotivationAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('text',)