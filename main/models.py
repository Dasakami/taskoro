from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL  
from datetime import date

class DailyMission(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    experience_reward = models.IntegerField(default=50)
    coins_reward = models.IntegerField(default=10)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_missions')
    date_created = models.DateField(default=date.today)
    date_completed = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    def complete_mission(self):
        if not self.is_completed:
            self.is_completed = True
            self.date_completed = date.today()
            
            profile = self.assigned_to.profile
            profile.add_experience(self.experience_reward)
            profile.coins += self.coins_reward
            profile.save()
            
            self.save()
            return True
        return False

class DailyMotivation(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.text[:50] + ('...' if len(self.text) > 50 else '')
    
    class Meta:
        ordering = ['?'] 