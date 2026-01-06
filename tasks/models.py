from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL  
from django.utils import timezone
from users.models import CharacterClass


class TaskCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default="#6633ff")  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_categories')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория задачи'
        verbose_name_plural = "Категории задач"


class BaseTask(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Легкая'),
        ('medium', 'Средняя'),
        ('hard', 'Сложная'),
        ('epic', 'Эпическая'),
    ]
    
    TASK_TYPE_CHOICES = [
        ('one_time', 'Одноразовая задача'),
        ('habit', 'Привычка'),
        ('daily', 'Цель на день'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE, related_name='base_tasks')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    task_type = models.CharField(max_length=15, choices=TASK_TYPE_CHOICES, default='one_time')
    estimated_minutes = models.IntegerField(default=30, help_text="Estimated time to complete in minutes")
    xp_reward = models.IntegerField(default=20, help_text="Base XP reward for completing this task")

    class Meta:
        verbose_name = 'Базовая задача'
        verbose_name_plural = "Базовые задачи"
    
    def __str__(self):
        return f"{self.title} ({self.get_task_type_display()}, {self.character_class.name})"


class BaseTaskCompletion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='completed_base_tasks')
    base_task = models.ForeignKey(BaseTask, on_delete=models.CASCADE, related_name='completions')
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Выполнение базовой задачи'
        verbose_name_plural = 'Выполнение базовых задач'
        ordering = ['-completed_at']
    
    def __str__(self):
        return f"{self.user.username} completed {self.base_task.title} at {self.completed_at}"


class Task(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Легкая'),
        ('medium', 'Средняя'),
        ('hard', 'Сложная'),
        ('epic', 'Эпическая'),
    ]
    
    STATUS_CHOICES = [
        ('not_started', 'Не начата'),
        ('in_progress', 'В процессе'),
        ('waiting', 'Ожидает'),
        ('completed', 'Завершена'),
    ]
    
    TASK_TYPE_CHOICES = [
        ('one_time', 'Одноразовая задача'),
        ('habit', 'Привычка'),
        ('daily', 'Цель на день'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    category = models.ForeignKey(TaskCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    character_class = models.ForeignKey(CharacterClass, on_delete=models.SET_NULL, null=True, blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='not_started')
    task_type = models.CharField(max_length=15, choices=TASK_TYPE_CHOICES, default='one_time')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    estimated_minutes = models.IntegerField(default=30, help_text="Estimated time to complete in minutes")
    actual_minutes = models.IntegerField(null=True, blank=True, help_text="Actual time taken to complete in minutes")
    
    # Для привычек
    frequency = models.CharField(max_length=20, default='daily', 
                                help_text="How often this habit should be performed")
    streak = models.IntegerField(default=0, help_text="Current streak for this habit")
    last_completed = models.DateField(null=True, blank=True)
    
    # Для ежедневных целей
    target_date = models.DateField(null=True, blank=True, help_text="The date this task is targeted for")
    
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def complete_task(self):
        """
        Отметить задачу как выполненную и начислить награды
        Возвращает количество полученного опыта
        """
        if self.is_completed:
            return 0
            
        self.is_completed = True
        self.status = 'completed'
        self.completed_at = timezone.now()
        
        # Награды в зависимости от сложности
        exp_rewards = {
            'easy': 20,
            'medium': 40,
            'hard': 80,
            'epic': 150,
        }
        
        experience = exp_rewards.get(self.difficulty, 30)
        
        # Бонус за выполнение до дедлайна
        if self.deadline and timezone.now() < self.deadline:
            experience += 15
        
        # Обработка привычек
        if self.task_type == 'habit':
            today = timezone.now().date()
            
            if self.last_completed:
                yesterday = today - timezone.timedelta(days=1)
                if self.last_completed == yesterday:
                    self.streak += 1
                elif self.last_completed != today:
                    self.streak = 1
            else:
                self.streak = 1
            
            self.last_completed = today

            # Бонус за серию
            if self.streak >= 7:
                experience += 10
            if self.streak >= 30:
                experience += 20

        # Начисляем награды пользователю
        profile = self.user.profile
        profile.add_experience(experience)
        coins = int(experience / 4)
        profile.coins += coins
        profile.save()
        
        self.save()
        return experience
    
    def get_difficulty_color(self):
        colors = {
            'easy': '#33ff99',
            'medium': '#ffcc33',
            'hard': '#ff3366',
            'epic': '#6633ff',
        }
        return colors.get(self.difficulty, '#6633ff')
    
    def is_overdue(self):
        if self.deadline and not self.is_completed:
            return timezone.now() > self.deadline
        return False
    
    def get_status_display_custom(self):
        if self.is_completed:
            return 'Завершена'
        elif self.is_overdue():
            return 'Просрочена'
        else:
            return dict(self.STATUS_CHOICES).get(self.status)