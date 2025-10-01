from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import DailyMission, DailyMotivation
from tasks.models import Task
from tournaments.models import Tournament
from users.models import Profile
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import random

def main(request):
    today = timezone.now().date()

    profile = None
    daily_mission = None
    recent_tasks = []
    completed_tasks_today = 0

    if request.user.is_authenticated:
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = None

        daily_mission = DailyMission.objects.filter(
            assigned_to=request.user,
            date_created=today,
            is_completed=False
        ).first()

        if not daily_mission:
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

        recent_tasks = Task.objects.filter(
            user=request.user
        ).order_by('-created_at')[:5]

        completed_tasks_today = Task.objects.filter(
            user=request.user,
            completed_at__date=today,
            is_completed=True
        ).count()

    daily_motivation = DailyMotivation.objects.filter(is_active=True).order_by('?').first()
    if not daily_motivation:
        daily_motivation = {
            'text': "Магия внутри тебя сильнее, чем ты думаешь. Используй ее для достижения целей!",
            'author': "Древний манускрипт"
        }

    active_tournaments = Tournament.objects.filter(
        end_date__gte=today
    ).order_by('end_date')[:3]

    context = {
        'profile': profile,
        'daily_mission': daily_mission,
        'daily_motivation': daily_motivation,
        'recent_tasks': recent_tasks,
        'active_tournaments': active_tournaments,
        'completed_tasks_today': completed_tasks_today,
        'total_tasks_today': len(recent_tasks),
    }

    return render(request, 'main/main.html', context)


def complete_mission(request, mission_id):
    mission = get_object_or_404(DailyMission, id=mission_id, assigned_to=request.user)
    
    if mission.complete_mission():
        messages.success(request, f'Миссия "{mission.title}" выполнена! Получено {mission.experience_reward} XP и {mission.coins_reward} монет.')
    else:
        messages.info(request, 'Эта миссия уже была выполнена ранее.')
    
    return redirect('main')


def page_not_found(request, exception):
    return render(request, '404.html', status=404)

def server_error(request):
    return render(request, '500.html', status=500)

def permission_denied(request, exception):
    return render(request, '403.html', status=403)

def bad_request(request, exception):
    return render(request, '400.html', status=400)


@login_required
def custom_upload_function(request):
    if request.method == 'POST' and request.FILES.get('upload'):
        file = request.FILES['upload']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file) 
        file_url = fs.url(filename) 
        return JsonResponse({
            'uploaded': 1,
            'fileName': filename,
            'url': file_url
        })
    return JsonResponse({'uploaded': 0})

def admin_rofl(request):
    return render(request, 'main/admin_rofl.html')
