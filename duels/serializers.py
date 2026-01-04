from rest_framework import serializers
from .models import Duel, DuelProgress
from django.conf import settings
User = settings.AUTH_USER_MODEL  
from django.shortcuts import get_object_or_404


class DuelUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        ref_name = 'DuelsUser'


        def create(self, validated_data):
            challenger_id = validated_data.pop('challenger_id')
            challenger = User.objects.get(pk=challenger_id)
            return Duel.objects.create(challenger=challenger, **validated_data)



class DuelSerializer(serializers.ModelSerializer):
    challenger = DuelUserSerializer(read_only=True)
    opponent = DuelUserSerializer(read_only=True)

    opponent_id = serializers.IntegerField(write_only=True)
    task = serializers.IntegerField(write_only=True)
    coins_stake = serializers.IntegerField()

    class Meta:
        model = Duel
        fields = [
            'id', 'challenger', 'opponent',
            'opponent_id', 'task', 'coins_stake',
            'status', 'created_at', 'start_time', 'end_time', 'winner',
        ]
        read_only_fields = [
            'id', 'challenger', 'opponent',
            'status', 'created_at', 'start_time', 'end_time', 'winner',
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        opponent = get_object_or_404(User, pk=validated_data.pop('opponent_id'))
        task_pk = validated_data.pop('task')
        duel = Duel.objects.create(
            challenger=user,
            opponent=opponent,
            task_id=task_pk,
            **validated_data
        )
        return duel

class DuelProgressSerializer(serializers.ModelSerializer):
    user = DuelUserSerializer(read_only=True)

    class Meta:
        model = DuelProgress
        fields = ['id', 'duel', 'user', 'completed', 'completion_time']

class DuelHistorySerializer(serializers.ModelSerializer):
    challenger = DuelUserSerializer(read_only=True)
    opponent = DuelUserSerializer(read_only=True)
    winner = DuelUserSerializer(read_only=True)

    class Meta:
        model = Duel
        fields = [
            'id', 'challenger', 'opponent', 'task', 'coins_stake',
            'status', 'created_at', 'start_time', 'end_time', 'winner'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'start_time', 'end_time']
