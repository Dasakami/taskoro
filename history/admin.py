from django.contrib import admin
from .models import Achievement, ActivityLog, UserAchievement
admin.site.register(Achievement)
admin.site.register(ActivityLog)
admin.site.register(UserAchievement)
# Register your models here.
