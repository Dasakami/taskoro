from rest_framework import serializers
from .models import Task, BaseTask, TaskCategory, BaseTaskCompletion
from django.utils import timezone as tz


class TaskCategorySerializer(serializers.ModelSerializer):
    tasks_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = TaskCategory
        fields = ['id', 'name', 'tasks_count', 'description', 'color']
        read_only_fields = ['tasks_count']


class TaskSerializer(serializers.ModelSerializer):
    # Награды рассчитываются автоматически на основе сложности
    coins = serializers.SerializerMethodField(read_only=True)
    experience_reward = serializers.SerializerMethodField(read_only=True)
    
    is_completed = serializers.BooleanField(read_only=True)
    completed_at = serializers.DateTimeField(read_only=True)
    streak = serializers.IntegerField(read_only=True)
    last_completed = serializers.DateField(read_only=True)
    
    # Делаем поля опциональными
    deadline = serializers.DateTimeField(required=False, allow_null=True)
    target_date = serializers.DateField(required=False, allow_null=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=TaskCategory.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'task_type', 'difficulty',
            'status', 'deadline', 'created_at', 'updated_at', 'category',
            'is_completed', 'completed_at', 'estimated_minutes',
            'frequency', 'streak', 'last_completed', 'target_date',
            'coins', 'experience_reward', 'character_class'
        ]
        read_only_fields = ['created_at', 'updated_at', 'is_completed', 
                           'completed_at', 'streak', 'last_completed',
                           'coins', 'experience_reward']

    def get_coins(self, obj):
        """Монеты = опыт / 4"""
        exp_rewards = {
            'easy': 20,
            'medium': 40,
            'hard': 80,
            'epic': 150,
        }
        experience = exp_rewards.get(obj.difficulty, 30)
        return int(experience / 4)
    
    def get_experience_reward(self, obj):
        """Награда опытом зависит от сложности"""
        exp_rewards = {
            'easy': 20,
            'medium': 40,
            'hard': 80,
            'epic': 150,
        }
        return exp_rewards.get(obj.difficulty, 30)
    
    def validate(self, data):
        """Валидация данных перед сохранением"""
        # Убедимся что обязательные поля присутствуют
        if not data.get('title'):
            raise serializers.ValidationError({'title': 'Название задачи обязательно'})
        
        # Для deadline добавляем timezone если отсутствует
        if 'deadline' in data and data['deadline']:
            if data['deadline'].tzinfo is None:
                data['deadline'] = tz.make_aware(data['deadline'])
        
        # Устанавливаем значения по умолчанию если не переданы
        if 'description' not in data:
            data['description'] = ''
        
        if 'status' not in data:
            data['status'] = 'not_started'
        
        if 'estimated_minutes' not in data:
            data['estimated_minutes'] = 30
        
        return data


class BaseTaskSerializer(serializers.ModelSerializer):
    character_class_name = serializers.CharField(source='character_class.name', read_only=True)
    coins = serializers.SerializerMethodField(read_only=True)
    # Добавляем поле completed для frontend
    completed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BaseTask
        fields = [
            'id', 'title', 'description', 'task_type', 'difficulty',
            'character_class', 'character_class_name', 'xp_reward',
            'estimated_minutes', 'coins', 'completed'
        ]

    def get_coins(self, obj):
        """Монеты = опыт / 4"""
        return int(obj.xp_reward / 4)
    
    def get_completed(self, obj):
        """Проверяем, выполнена ли задача сегодня текущим пользователем"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            today = tz.now().date()
            return BaseTaskCompletion.objects.filter(
                user=request.user,
                base_task=obj,
                completed_at__date=today
            ).exists()
        return False


class BaseTaskCompletionSerializer(serializers.ModelSerializer):
    base_task = BaseTaskSerializer(read_only=True)
    
    class Meta:
        model = BaseTaskCompletion
        fields = ['id', 'base_task', 'completed_at']