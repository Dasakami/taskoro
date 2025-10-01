
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ActivityLog, Achievement, UserAchievement

@login_required
def activity_log(request):
    activities = ActivityLog.objects.filter(user=request.user)

    activity_type = request.GET.get('type')
    if activity_type:
        activities = activities.filter(activity_type=activity_type)
    
    context = {
        'activities': activities,
        'activity_types': ActivityLog.ACTIVITY_TYPES,
    }
    
    return render(request, 'history/activity_log.html', context)

@login_required
def achievement_list(request):
    achievements = Achievement.objects.all()
    user_achievements = UserAchievement.objects.filter(user=request.user)
    acquired_achievements = set(ua.achievement_id for ua in user_achievements)
    
    for achievement in achievements:
        achievement.is_acquired = achievement.id in acquired_achievements
    
    context = {
        'achievements': achievements,
        'acquired_count': len(acquired_achievements),
        'total_count': achievements.count(),
    }
    
    return render(request, 'history/achievement_list.html', context)
