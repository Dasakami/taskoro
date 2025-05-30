from rest_framework import serializers
from .models import Task, BaseTask, TaskCategory, BaseTaskCompletion

class TaskCategorySerializer(serializers.ModelSerializer):
    tasks_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = TaskCategory
        fields = ['id', 'name', 'tasks_count']

class TaskSerializer(serializers.ModelSerializer):
    coins = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'task_type', 'difficulty',
            'status', 'deadline', 'created_at', 'updated_at', 'category',
            'coins'  # теперь работает корректно
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_coins(self, obj):
        # Получаем coins из профиля пользователя, связанного с задачей
        return getattr(obj.user.profile, 'coins', 0)
    
class BaseTaskSerializer(serializers.ModelSerializer):
    character_class_name = serializers.CharField(source='character_class.name', read_only=True)

    class Meta:
        model = BaseTask
        fields = [
            'id', 'title', 'description', 'task_type', 'difficulty',
            'character_class', 'character_class_name', 'xp_reward'
        ]

class BaseTaskCompletionSerializer(serializers.ModelSerializer):
    base_task = BaseTaskSerializer(read_only=True)
    
    class Meta:
        model = BaseTaskCompletion
        fields = ['id', 'base_task', 'completed_at']
