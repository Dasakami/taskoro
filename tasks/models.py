from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class TaskCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default="#6633ff")  # Hex color code
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_categories')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Task Categories"

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
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    category = models.ForeignKey(TaskCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='not_started')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    estimated_minutes = models.IntegerField(default=30, help_text="Estimated time to complete in minutes")
    actual_minutes = models.IntegerField(null=True, blank=True, help_text="Actual time taken to complete in minutes")
    
    def __str__(self):
        return self.title
    
    def complete_task(self):
        if not self.is_completed:
            self.is_completed = True
            self.status = 'completed'
            self.completed_at = timezone.now()
            
            # Calculate experience based on difficulty
            exp_rewards = {
                'easy': 20,
                'medium': 40,
                'hard': 80,
                'epic': 150,
            }
            
            experience = exp_rewards.get(self.difficulty, 30)
            
            # If completed before deadline, add bonus
            if self.deadline and timezone.now() < self.deadline:
                experience += 15
            
            # Reward user with experience and coins
            profile = self.user.profile
            profile.add_experience(experience)
            profile.coins += int(experience / 4)  # Coins are roughly 1/4 of exp
            profile.save()
            
            self.save()
            return experience
        return 0
    
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