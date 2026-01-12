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
        """
        POST /api/tasks/tasks/{id}/complete/
        Отметить задачу как выполненную
        """
        task = self.get_object()
        
        if task.is_completed:
            return Response({
                'detail': 'Задача уже была выполнена ранее.',
                'task': self.get_serializer(task).data
            }, status=status.HTTP_400_BAD_REQUEST)
        
        experience = task.complete_task()
        
        if experience > 0:
            serializer = self.get_serializer(task)
            return Response({
                'detail': f'Задача "{task.title}" выполнена! Получено {experience} XP.',
                'task': serializer.data,
                'xp': experience,
                'coins': int(experience / 4)
            })
        else:
            return Response({
                'detail': 'Ошибка при выполнении задачи'
            }, status=status.HTTP_400_BAD_REQUEST)


class BaseTaskViewSet(viewsets.ModelViewSet):
    serializer_class = BaseTaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_classes = self.request.user.profile.character_classes.all()
        return BaseTask.objects.filter(character_class__in=user_classes)
    
    def get_serializer_context(self):
        """Добавляем request в контекст для проверки статуса выполнения"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """
        POST /api/tasks/base-tasks/{id}/complete/
        Выполнить базовую задачу
        """
        base_task = self.get_object()

        if not request.user.profile.character_classes.filter(id=base_task.character_class.id).exists():
            return Response({
                'detail': 'Нет доступа к этому заданию'
            }, status=status.HTTP_403_FORBIDDEN)

        today = timezone.now().date()
        
        # Проверяем, не выполнена ли задача сегодня
        existing_completion = BaseTaskCompletion.objects.filter(
            user=request.user,
            base_task=base_task,
            completed_at__date=today
        ).first()
        
        if existing_completion:
            return Response({
                'detail': 'Задача уже выполнена сегодня'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Создаем запись о выполнении
        completion = BaseTaskCompletion.objects.create(
            user=request.user,
            base_task=base_task,
            completed_at=timezone.now()
        )

        # Начисляем награды
        profile = request.user.profile
        experience = base_task.xp_reward
        coins = int(experience / 4)
        
        profile.add_experience(experience)
        profile.coins += coins
        profile.save()

        return Response({
            'detail': f'Задача "{base_task.title}" выполнена! Получено {experience} XP и {coins} монет.',
            'xp': experience,
            'coins': coins,
            'completed': True
        })


class BaseTaskCompletionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BaseTaskCompletionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BaseTaskCompletion.objects.filter(user=self.request.user).order_by('-completed_at')


class TaskCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = TaskCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TaskCategory.objects.filter(user=self.request.user).annotate(tasks_count=Count('tasks'))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)