from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Duel, DuelProgress
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .serializers import DuelSerializer, DuelProgressSerializer, DuelHistorySerializer



class DuelViewSet(viewsets.ModelViewSet):
    serializer_class = DuelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Duel.objects.filter(
            Q(challenger=user) | Q(opponent=user)
        ).order_by('-created_at')

    def get_serializer_context(self):
        return {'request': self.request}
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        duel = get_object_or_404(Duel, pk=pk)
        try:
            duel.accept_duel(request.user)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(duel).data)

    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        duel = get_object_or_404(Duel, pk=pk)
        try:
            duel.decline_duel(request.user)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'declined'})



class DuelProgressViewSet(viewsets.ModelViewSet):
    queryset         = DuelProgress.objects.all()
    serializer_class = DuelProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        prog = get_object_or_404(DuelProgress, pk=pk, user=request.user)
        prog.complete_task()
        return Response({'status': 'task completed'})


class DuelHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Duel.objects.all()
    serializer_class = DuelHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Duel.objects.filter(
            Q(challenger=user) | Q(opponent=user)
        ).order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

