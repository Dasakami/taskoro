from django.db import models
from django.contrib.auth.models import User
from tasks.models import Task
from django.utils import timezone

class Duel(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает принятия'),
        ('active', 'В процессе'),
        ('completed', 'Завершена'),
        ('declined', 'Отклонена'),
    ]
    
    challenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='duels_as_challenger')
    opponent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='duels_as_opponent')
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True)
    coins_stake = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='duels_won')
    
    def __str__(self):
        return f"{self.challenger.username} vs {self.opponent.username}"
    
    def start_duel(self):
        if self.status == 'pending':
            self.status = 'active'
            self.start_time = timezone.now()
            self.save()
    
    def complete_duel(self, winner):
        if self.status == 'active':
            self.status = 'completed'
            self.end_time = timezone.now()
            self.winner = winner
            
            # Transfer stakes
            if self.coins_stake > 0:
                loser = self.opponent if winner == self.challenger else self.challenger
                winner.profile.coins += self.coins_stake * 2
                winner.profile.save()
            
            # Award experience
            winner.profile.add_experience(50)  # Base experience for winning
            self.save()
    
    def decline_duel(self):
        if self.status == 'pending':
            self.status = 'declined'
            self.save()
            
            # Return stakes to challenger
            if self.coins_stake > 0:
                self.challenger.profile.coins += self.coins_stake
                self.challenger.profile.save()

class DuelProgress(models.Model):
    duel = models.ForeignKey(Duel, on_delete=models.CASCADE, related_name='progress')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completion_time = models.DateTimeField(null=True, blank=True)
    
    def complete_task(self):
        if not self.completed:
            self.completed = True
            self.completion_time = timezone.now()
            self.save()
            
            # Check if this completes the duel
            opponent_progress = self.duel.progress.exclude(id=self.id).first()
            if opponent_progress and opponent_progress.completed:
                # Determine winner based on completion time
                if self.completion_time < opponent_progress.completion_time:
                    self.duel.complete_duel(self.user)
                else:
                    self.duel.complete_duel(opponent_progress.user)