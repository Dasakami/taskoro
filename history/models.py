from django.db import models
from django.contrib.auth.models import User
from tasks.models import Task
from duels.models import Duel
from tournaments.models import Tournament

class ActivityLog(models.Model):
    ACTIVITY_TYPES = [
        ('task_complete', 'Завершение задачи'),
        ('tournament_join', 'Участие в турнире'),
        ('tournament_win', 'Победа в турнире'),
        ('duel_complete', 'Завершение дуэли'),
        ('chest_open', 'Открытие сундука'),
        ('level_up', 'Повышение уровня'),
        ('achievement', 'Получение достижения'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.TextField()
    experience_gained = models.IntegerField(default=0)
    coins_gained = models.IntegerField(default=0)
    gems_gained = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.SET_NULL, null=True, blank=True)
    duel = models.ForeignKey(Duel, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_activity_type_display()}"


class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)  
    experience_reward = models.IntegerField(default=0)
    coins_reward = models.IntegerField(default=0)
    gems_reward = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    acquired_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'achievement')
    
    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"