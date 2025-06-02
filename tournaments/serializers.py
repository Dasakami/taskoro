from rest_framework import serializers
from .models import Tournament, TournamentParticipant

class TournamentSerializer(serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField()
    
    class Meta:
        model = Tournament
        fields = '__all__'

    def get_is_active(self, obj):
        return obj.is_active()

class ParticipantSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = TournamentParticipant
        fields = ['id', 'user', 'user_username', 'score', 'tasks_completed', 'joined_at', 'last_updated']
