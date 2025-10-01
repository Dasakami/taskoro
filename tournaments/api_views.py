from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Tournament,TournamentParticipant
from .serializers import TournamentSerializer, ParticipantSerializer
from history.models import ActivityLog

class TournamentListAPI(generics.ListAPIView):
    queryset = Tournament.objects.all().order_by('-start_date')
    serializer_class = TournamentSerializer
    permission_classes = [permissions.AllowAny]

class TournamentDetailAPI(generics.RetrieveAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    lookup_field = 'id'
    permission_classes = [permissions.AllowAny]

class TournamentLeaderboardAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, id):
        tournament = get_object_or_404(Tournament, id=id)
        leaderboard = tournament.get_leaderboard()
        serializer = ParticipantSerializer(leaderboard, many=True)
        return Response(serializer.data)

class JoinTournamentAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        tournament = get_object_or_404(Tournament, id=id)

        if not tournament.is_active():
            return Response({'error': 'Турнир не активен.'}, status=status.HTTP_400_BAD_REQUEST)

        participant, created = TournamentParticipant.objects.get_or_create(
            tournament=tournament,
            user=request.user,
        )

        if created:
            ActivityLog.objects.create(
                user=request.user,
                activity_type='tournament_join',
                description=f'Вы участвуете в турнире: {tournament.title}',
                tournament=tournament,
                experience_gained=tournament.experience_reward,
                coins_gained=tournament.coins_reward,
                gems_gained=tournament.gems_reward,
            )
            return Response({'message': 'Участие подтверждено.'}, status=201)
        else:
            return Response({'message': 'Вы уже участвуете в турнире.'}, status=200)