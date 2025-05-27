from rest_framework import serializers
from .models import ActivityLog, Achievement

class ActivityLogSerializer(serializers.ModelSerializer):
    activity_type_display = serializers.CharField(source='get_activity_type_display', read_only=True)
    class Meta:
        model = ActivityLog
        fields = [
            'id', 'activity_type', 'activity_type_display', 'description',
            'experience_gained', 'coins_gained', 'gems_gained', 'created_at',
        ]

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = [
            'id', 'name', 'description', 'icon',
            'experience_reward', 'coins_reward', 'gems_reward',
        ]
