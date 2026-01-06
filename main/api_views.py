from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from tasks.models import Task
from tournaments.models import Tournament
from .models import DailyMission, DailyMotivation
import random


class MainPageAPIView(APIView):
    """
    GET /api/main/
    Получить данные для главной страницы:
    - Профиль пользователя
    - Ежедневная миссия
    - Мотивация дня
    - Последние задачи
    - Выполненные задачи сегодня
    - Активные турниры
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = timezone.now().date()

        # Получить или создать дневную миссию
        mission, _ = DailyMission.objects.get_or_create(
            assigned_to=user,
            date_created=today,
            defaults={
                'title': random.choice([
                    "Покорите вершину знаний",
                    "Изучите древние руны",
                    "Пройдите испытание огнем",
                    "Раскройте тайны магии",
                    "Завершите ритуал посвящения"
                ]),
                'description': random.choice([
                    "Выполните 3 задачи сегодня",
                    "Создайте и выполните новую задачу",
                    "Сохраняйте фокус в течение 2 часов",
                    "Помогите другому Охотнику (добавьте в друзья)",
                    "Примите участие в турнире или дуэли"
                ]),
                'experience_reward': random.randint(40, 100),
                'coins_reward': random.randint(5, 15)
            }
        )

        # Получить мотивацию дня
        motivation = DailyMotivation.objects.filter(is_active=True).order_by('?').first()
        if not motivation:
            motivation_data = {
                'text': "Магия внутри тебя сильнее, чем ты думаешь.",
                'author': "Древний манускрипт"
            }
        else:
            motivation_data = {
                'text': motivation.text,
                'author': motivation.author or "Неизвестный"
            }

        # Последние 5 задач
        recent_tasks_qs = Task.objects.filter(user=user).order_by('-created_at')[:5]
        recent_tasks = [
            {
                'id': t.id,
                'title': t.title,
                'is_completed': t.is_completed,
                'difficulty': t.difficulty,
                'task_type': t.task_type
            }
            for t in recent_tasks_qs
        ]

        # Выполненные задачи сегодня
        completed_today = Task.objects.filter(
            user=user,
            is_completed=True,
            completed_at__date=today
        ).count()

        # Активные турниры
        tournaments = Tournament.objects.filter(end_date__gte=today).order_by('end_date')[:3]
        tournaments_data = [
            {
                'id': t.id,
                'title': t.title,
                'end_date': t.end_date.isoformat() if hasattr(t.end_date, 'isoformat') else str(t.end_date)
            }
            for t in tournaments
        ]

        return Response({
            'profile': {
                'username': user.username,
                'level': user.profile.level,
                'experience': user.profile.experience,
                'experience_needed': user.profile.experience_needed,
                'coins': user.profile.coins,
                'gems': user.profile.gems,
                'streak': user.profile.streak
            },
            'daily_mission': {
                'id': mission.id,
                'title': mission.title,
                'description': mission.description,
                'experience_reward': mission.experience_reward,
                'coins_reward': mission.coins_reward,
                'is_completed': mission.is_completed
            },
            'daily_motivation': motivation_data,
            'recent_tasks': recent_tasks,
            'completed_tasks_today': completed_today,
            'total_tasks_today': len(recent_tasks),
            'active_tournaments': tournaments_data
        })