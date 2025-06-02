from django.urls import path
from .api_views import (
    TournamentListAPI,
    TournamentDetailAPI,
    JoinTournamentAPI,
    TournamentLeaderboardAPI
)

urlpatterns = [
    path('', TournamentListAPI.as_view(), name='api_list'),
    path('<int:id>/', TournamentDetailAPI.as_view(), name='api_detail'),
    path('<int:id>/join/', JoinTournamentAPI.as_view(), name='api_join'),
    path('<int:id>/leaderboard/', TournamentLeaderboardAPI.as_view(), name='api_leaderboard'),
]
