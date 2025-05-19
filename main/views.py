from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import DailyMission, DailyMotivation
from tasks.models import Task
from tournaments.models import Tournament
import random

@login_required
def main(request):
    # Get user profile
    profile = request.user.profile
    
    # Get or create daily mission
    today = timezone.now().date()
    daily_mission = DailyMission.objects.filter(
        assigned_to=request.user,
        date_created=today,
        is_completed=False
    ).first()
    
    if not daily_mission:
        # Create a new daily mission (simplified)
        mission_titles = [
            "Покорите вершину знаний",
            "Изучите древние руны",
            "Пройдите испытание огнем",
            "Раскройте тайны магии",
            "Завершите ритуал посвящения"
        ]
        mission_descriptions = [
            "Выполните 3 задачи сегодня",
            "Создайте и выполните новую задачу",
            "Сохраняйте фокус в течение 2 часов",
            "Помогите другому Охотнику (добавьте в друзья)",
            "Примите участие в турнире или дуэли"
        ]
        
        # Randomly select mission details
        title = random.choice(mission_titles)
        description = random.choice(mission_descriptions)
        exp_reward = random.randint(40, 100)
        coins_reward = random.randint(5, 15)
        
        daily_mission = DailyMission.objects.create(
            title=title,
            description=description,
            experience_reward=exp_reward,
            coins_reward=coins_reward,
            assigned_to=request.user
        )
    
    # Get daily motivation
    daily_motivation = DailyMotivation.objects.filter(is_active=True).order_by('?').first()
    if not daily_motivation:
        # Fallback motivation
        daily_motivation = {
            'text': "Магия внутри тебя сильнее, чем ты думаешь. Используй ее для достижения целей!",
            'author': "Древний манускрипт"
        }
    
    # Get recent tasks
    recent_tasks = Task.objects.filter(
        user=request.user
    ).order_by('-created_at')[:5]
    
    # Get active tournaments
    active_tournaments = Tournament.objects.filter(
        end_date__gte=today
    ).order_by('end_date')[:3]
    
    # Get daily statistics
    completed_tasks_today = Task.objects.filter(
        user=request.user,
        completed_at__date=today,
        is_completed=True
    ).count()
    
    context = {
        'profile': profile,
        'daily_mission': daily_mission,
        'daily_motivation': daily_motivation,
        'recent_tasks': recent_tasks,
        'active_tournaments': active_tournaments,
        'completed_tasks_today': completed_tasks_today,
        'total_tasks_today': recent_tasks.count(),
    }
    
    return render(request, 'main/main.html', context)


def complete_mission(request, mission_id):
    mission = get_object_or_404(DailyMission, id=mission_id, assigned_to=request.user)
    
    if mission.complete_mission():
        messages.success(request, f'Миссия "{mission.title}" выполнена! Получено {mission.experience_reward} XP и {mission.coins_reward} монет.')
    else:
        messages.info(request, 'Эта миссия уже была выполнена ранее.')
    
    return redirect('main')