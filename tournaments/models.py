from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL  # можно использовать в type hints

from django.utils import timezone

class Tournament(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    experience_reward = models.IntegerField(default=200)
    coins_reward = models.IntegerField(default=50)
    gems_reward = models.IntegerField(default=5)
    
    min_tasks_completed = models.IntegerField(default=5, help_text="Minimum number of tasks to complete")
    
    def __str__(self):
        return self.title
    
    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date
    
    def has_started(self):
        return timezone.now() >= self.start_date
    
    def has_ended(self):
        return timezone.now() > self.end_date
    
    def get_participants_count(self):
        return self.participants.count()
    
    def get_leaderboard(self):
        return self.participants.order_by('-score', 'last_updated')
    
    def get_winners(self, top=3):
        if not self.has_ended():
            return []
        
        return self.get_leaderboard()[:top]

class TournamentParticipant(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tournament_participations')
    score = models.IntegerField(default=0)
    tasks_completed = models.IntegerField(default=0)
    joined_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('tournament', 'user')
    
    def __str__(self):
        return f"{self.user.username} in {self.tournament.title}"
    
    def update_score(self, new_task_count=1):
        self.tasks_completed += new_task_count
        self.score = self.tasks_completed * 10  
        self.save()
    
    def get_rank(self):
        participants = self.tournament.get_leaderboard()
        for i, participant in enumerate(participants):
            if participant.id == self.id:
                return i + 1
        return None