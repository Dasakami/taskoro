from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Duel, DuelProgress
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .serializers import DuelSerializer, DuelProgressSerializer
from duels import serializers


class DuelViewSet(viewsets.ModelViewSet):
    queryset = Duel.objects.all()
    serializer_class = DuelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Duel.objects.filter(
            Q(challenger=user) | Q(opponent=user)
        ).order_by('-created_at')

    def perform_create(self, serializer):
        opponent = self.request.data.get('opponent')
        task = self.request.data.get('task')
        coins_stake = int(self.request.data.get('coins_stake', 0))

        if self.request.user.profile.coins < coins_stake:
            raise serializers.ValidationError("Недостаточно монет")

        duel = serializer.save(
            challenger=self.request.user,
            opponent_id=opponent,
            task_id=task,
            coins_stake=coins_stake
        )

        # Списываем монеты
        if coins_stake > 0:
            self.request.user.profile.coins -= coins_stake
            self.request.user.profile.save()

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        duel = get_object_or_404(Duel, pk=pk, opponent=request.user, status='pending')

        if duel.coins_stake > request.user.profile.coins:
            return Response({'error': 'Недостаточно монет'}, status=400)

        # Списать монеты
        if duel.coins_stake > 0:
            request.user.profile.coins -= duel.coins_stake
            request.user.profile.save()

        duel.start_duel()
        DuelProgress.objects.create(duel=duel, user=duel.challenger)
        DuelProgress.objects.create(duel=duel, user=duel.opponent)

        return Response({'status': 'Дуэль принята'})

    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        duel = get_object_or_404(Duel, pk=pk, opponent=request.user, status='pending')
        duel.decline_duel()
        return Response({'status': 'Дуэль отклонена'})

class DuelProgressViewSet(viewsets.ModelViewSet):
    queryset = DuelProgress.objects.all()
    serializer_class = DuelProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        progress = get_object_or_404(DuelProgress, pk=pk, user=request.user, completed=False)
        progress.complete_task()
        return Response({'status': 'Задание выполнено'})
