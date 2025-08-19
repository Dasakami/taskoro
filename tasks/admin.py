from django.contrib import admin
from .models import Task, TaskCategory, BaseTask, BaseTaskCompletion

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'status', 'user', 'created_at', 'is_completed', 'task_type')
    list_filter = ('category', 'difficulty', 'status', 'is_completed', 'created_at', 'task_type')
    search_fields = ('title', 'description')

@admin.register(TaskCategory)
class TaskCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(BaseTask)
class BaseTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'character_class', 'difficulty', 'task_type', 'estimated_minutes', 'xp_reward')
    list_filter = ('character_class', 'difficulty', 'task_type')
    search_fields = ('title', 'description')

@admin.register(BaseTaskCompletion)
class BaseTaskCompletionAdmin(admin.ModelAdmin):
    list_display = ('user', 'base_task', 'completed_at')
    list_filter = ('user', 'base_task', 'completed_at')
    search_fields = ('user__username', 'base_task__title')