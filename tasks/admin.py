from django.contrib import admin
from .models import Task, TaskCategory

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'status', 'user', 'created_at', 'is_completed')
    list_filter = ('category', 'difficulty', 'status', 'is_completed', 'created_at')
    search_fields = ('title', 'description')

@admin.register(TaskCategory)
class TaskCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)