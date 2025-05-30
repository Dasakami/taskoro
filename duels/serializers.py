from rest_framework import serializers
from .models import Duel, DuelProgress
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class DuelSerializer(serializers.ModelSerializer):
    challenger = UserSerializer(read_only=True)
    opponent = UserSerializer(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Duel
        fields = [
            'id', 'challenger', 'opponent', 'task', 'coins_stake',
            'status', 'created_at', 'start_time', 'end_time', 'winner'
        ]

class DuelProgressSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = DuelProgress
        fields = ['id', 'duel', 'user', 'completed', 'completion_time']
