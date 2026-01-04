from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL  
from tasks.models import Task
from django.utils import timezone
from datetime import timedelta


class Duel(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Ожидает'),
        ('active',    'В процессе'),
        ('completed', 'Завершена'),
        ('declined',  'Отклонена'),
    ]

    challenger   = models.ForeignKey(User, related_name='duels_sent', on_delete=models.CASCADE)
    opponent     = models.ForeignKey(User, related_name='duels_received', on_delete=models.CASCADE)
    task         = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    coins_stake  = models.PositiveIntegerField(default=0)
    status       = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at   = models.DateTimeField(auto_now_add=True)
    start_time   = models.DateTimeField(null=True, blank=True)
    end_time     = models.DateTimeField(null=True, blank=True)
    winner       = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='duels_won')
    duration     = models.DurationField(default=timedelta(hours=24))  

    def __str__(self):
        return f"{self.challenger} vs {self.opponent} [{self.status}]"

    def accept_duel(self, user: User):
        """
        Вызывается оппонентом по /duels/{id}/accept/
        1) Проверить, что это действительно opponent и статус == pending
        2) Списать ставку у opponent
        3) Перевести в active, выставить start/end
        4) Создать две записи DuelProgress
        """
        if user != self.opponent:
            raise ValueError("Не ваш дуэль")
        if self.status != 'pending':
            raise ValueError("Дуэль уже не в состоянии pending")

        profile = user.profile
        if profile.coins < self.coins_stake:
            raise ValueError("Недостаточно монет для принятия")
        profile.coins -= self.coins_stake
        profile.save()
        now = timezone.now()
        self.status     = 'active'
        self.start_time = now
        self.end_time   = now + self.duration
        self.save()

        DuelProgress.objects.bulk_create([
            DuelProgress(duel=self, user=self.challenger),
            DuelProgress(duel=self, user=self.opponent),
        ])

    def decline_duel(self, user: User):
        """
        Вызывается оппонентом по /duels/{id}/decline/
        1) Проверить, что это opponent и статус == pending
        2) Перевести статус в declined
        3) Вернуть стейк challenger-у
        """
        if user != self.opponent:
            raise ValueError("Не ваш дуэль")
        if self.status != 'pending':
            raise ValueError("Нельзя отклонить не-pending дуэль")

        self.status = 'declined'
        self.save()

        if self.coins_stake > 0:
            init_profile = self.challenger.profile
            init_profile.coins += self.coins_stake
            init_profile.save()

    def complete_duel(self, winner: User):
        """
        Завершить дуэль вручную, например, при двух completed
        или таймауте.
        """
        if self.status != 'active':
            raise ValueError("Дуэль не в состоянии active")

        self.status   = 'completed'
        self.end_time = timezone.now()
        self.winner   = winner
        self.save()

        if self.coins_stake > 0:
            win_profile = winner.profile
            win_profile.coins += self.coins_stake * 2
            win_profile.save()

        winner.profile.add_experience(50)

class DuelProgress(models.Model):
    duel            = models.ForeignKey(Duel, related_name='progress', on_delete=models.CASCADE)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    completed       = models.BooleanField(default=False)
    completion_time = models.DateTimeField(null=True, blank=True)

    def complete_task(self):
        """
        Пользователь помечает задачу выполненной.
        Если оба отметились — завершаем дуэль по времени.
        """
        if self.completed:
            return

        self.completed = True
        self.completion_time = timezone.now()
        self.save()

        other = self.duel.progress.exclude(pk=self.pk).first()
        if other and other.completed:
            if self.completion_time <= other.completion_time:
                winner = self.user
            else:
                winner = other.user
            self.duel.complete_duel(winner)
