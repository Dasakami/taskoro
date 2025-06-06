from django.db import models
from django.contrib.auth.models import User
from users.models import Profile

class FriendRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает ответа'),
        ('accepted', 'Принят'),
        ('declined', 'Отклонен'),
    ]
    
    sender = models.ForeignKey(Profile, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Profile, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('sender', 'receiver')
    
    def __str__(self):
        return f"{self.sender.user.username} -> {self.receiver.user.username}"
    
    def accept(self):
        if self.status == 'pending':
            self.status = 'accepted'
            Friendship.create_friendship(self.sender.user, self.receiver.user)
            self.save()
    
    def decline(self):
        if self.status == 'pending':
            self.status = 'declined'
            self.save()

class Friendship(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships2')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user1', 'user2')
    
    def __str__(self):
        return f"{self.user1.username} - {self.user2.username}"
    
    @classmethod
    def are_friends(cls, user1, user2):
        return cls.objects.filter(
            models.Q(user1=user1, user2=user2) | 
            models.Q(user1=user2, user2=user1)
        ).exists()

    @classmethod
    def create_friendship(cls, user1, user2):
        if user1.id > user2.id:
            user1, user2 = user2, user1  # Для уникальности (user1 < user2)
        if not cls.are_friends(user1, user2):
            cls.objects.create(user1=user1, user2=user2)


class FriendActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}: {self.activity_type}"