from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ActivityLog, Achievement, UserAchievement
from .serializers import ActivityLogSerializer, AchievementSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def activity_log_api(request):
    activity_type = request.GET.get('type')
    logs = ActivityLog.objects.filter(user=request.user)
    if activity_type:
        logs = logs.filter(activity_type=activity_type)
    serializer = ActivityLogSerializer(logs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def achievement_list_api(request):
    achievements = Achievement.objects.all()
    acquired_ids = set(
        UserAchievement.objects.filter(user=request.user).values_list('achievement_id', flat=True)
    )

    serialized = []
    for achievement in achievements:
        data = AchievementSerializer(achievement).data
        data['is_acquired'] = achievement.id in acquired_ids
        serialized.append(data)

    return Response({
        'achievements': serialized,
        'acquired_count': len(acquired_ids),
        'total_count': achievements.count(),
    })
