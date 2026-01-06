from rest_framework import serializers
from .models import Task, BaseTask, TaskCategory, BaseTaskCompletion


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
        # Для одноразовых задач может быть deadline
        if data.get('task_type') == 'one_time' and 'deadline' in data:
            if data['deadline'] and data['deadline'].tzinfo is None:
                # Добавляем timezone если отсутствует
                from django.utils import timezone
                data['deadline'] = timezone.make_aware(data['deadline'])
        
        # Для ежедневных целей может быть target_date
        if data.get('task_type') == 'daily' and 'target_date' in data:
            # target_date это date, не datetime
            pass
        
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
            from django.utils import timezone
            today = timezone.now().date()
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