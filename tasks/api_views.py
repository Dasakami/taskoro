from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Task, BaseTask, TaskCategory, BaseTaskCompletion
from .serializers import TaskSerializer, BaseTaskSerializer, TaskCategorySerializer, BaseTaskCompletionSerializer
from django.db.models import Count

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        task = self.get_object()
        experience = task.complete_task()
        if experience > 0:
            return Response({'detail': f'Задача "{task.title}" выполнена! Получено {experience} XP.'})
        else:
            return Response({'detail': 'Задача уже была выполнена ранее.'}, status=status.HTTP_400_BAD_REQUEST)

class BaseTaskViewSet(viewsets.ModelViewSet):
    serializer_class = BaseTaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_classes = self.request.user.profile.character_classes.all()
        return BaseTask.objects.filter(character_class__in=user_classes)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        base_task = self.get_object()

        if not request.user.profile.character_classes.filter(id=base_task.character_class.id).exists():
            return Response({'detail': 'Нет доступа к этому заданию'}, status=status.HTTP_403_FORBIDDEN)

        today = timezone.now().date()
        if BaseTaskCompletion.objects.filter(user=request.user, base_task=base_task, completed_at__date=today).exists():
            return Response({'detail': 'Задача уже выполнена сегодня'}, status=status.HTTP_400_BAD_REQUEST)

        completion = BaseTaskCompletion.objects.create(
            user=request.user,
            base_task=base_task,
            completed_at=timezone.now()
        )

        profile = request.user.profile
        experience = base_task.xp_reward
        profile.add_experience(experience)
        profile.coins += int(experience / 4)
        profile.save()

        return Response({'detail': f'Задача "{base_task.title}" выполнена! Получено {experience} XP.'})


class BaseTaskCompletionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BaseTaskCompletionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BaseTaskCompletion.objects.filter(user=self.request.user).order_by('-completed_at')

    @action(detail=False, methods=['post'])
    def complete_task(self, request):
        base_task_id = request.data.get('base_task_id')
        if not base_task_id:
            return Response({'detail': 'base_task_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            base_task = BaseTask.objects.get(id=base_task_id)
        except BaseTask.DoesNotExist:
            return Response({'detail': 'Base task not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if not request.user.profile.character_classes.filter(id=base_task.character_class.id).exists():
            return Response({'detail': 'Нет доступа к этому заданию'}, status=status.HTTP_403_FORBIDDEN)

        today = timezone.now().date()
        if BaseTaskCompletion.objects.filter(user=request.user, base_task=base_task, completed_at__date=today).exists():
            return Response({'detail': 'Задача уже выполнена сегодня'}, status=status.HTTP_400_BAD_REQUEST)

        completion = BaseTaskCompletion.objects.create(
            user=request.user,
            base_task=base_task,
            completed_at=timezone.now()
        )

        profile = request.user.profile
        experience = base_task.xp_reward
        profile.add_experience(experience)
        profile.coins += int(experience / 4)
        profile.save()

        return Response({'detail': f'Задача "{base_task.title}" выполнена! Получено {experience} XP.'})

class TaskCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = TaskCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TaskCategory.objects.filter(user=self.request.user).annotate(tasks_count=Count('tasks'))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
