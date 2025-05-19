from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Tournament, TournamentParticipant


def tournament_list(request):
    # Get current date
    now = timezone.now()
    
    # Get active tournaments
    active_tournaments = Tournament.objects.filter(
        start_date__lte=now,
        end_date__gte=now
    ).order_by('end_date')
    
    # Get upcoming tournaments
    upcoming_tournaments = Tournament.objects.filter(
        start_date__gt=now
    ).order_by('start_date')
    
    # Get past tournaments
    past_tournaments = Tournament.objects.filter(
        end_date__lt=now
    ).order_by('-end_date')[:5]  # Limit to recent tournaments
    
    # Get user participations
    if request.user.is_authenticated:
        user_participations = TournamentParticipant.objects.filter(
            user=request.user
        ).values_list('tournament_id', flat=True)
    else:
        user_participations = []
    
    context = {
        'active_tournaments': active_tournaments,
        'upcoming_tournaments': upcoming_tournaments,
        'past_tournaments': past_tournaments,
        'user_participations': user_participations,
    }
    
    return render(request, 'tournaments/tournament_list.html', context)


def tournament_detail(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)

    is_participating = False
    participant = None
    user_rank = None

    if request.user.is_authenticated:
        try:
            participant = TournamentParticipant.objects.get(tournament=tournament, user=request.user)
            is_participating = True
            user_rank = participant.get_rank()
        except TournamentParticipant.DoesNotExist:
            pass

    leaderboard = tournament.get_leaderboard()

    context = {
        'tournament': tournament,
        'is_participating': is_participating,
        'participant': participant,
        'leaderboard': leaderboard,
        'user_rank': user_rank,
    }

    return render(request, 'tournaments/tournament_detail.html', context)


@login_required
def tournament_join(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    
    # Check if tournament is still active
    if not tournament.is_active():
        messages.error(request, 'Турнир уже завершен или еще не начался.')
        return redirect('tournaments:tournament_detail', tournament_id=tournament.id)
    
    # Check if user is already participating
    if TournamentParticipant.objects.filter(tournament=tournament, user=request.user).exists():
        messages.info(request, 'Вы уже участвуете в этом турнире.')
    else:
        # Join tournament
        TournamentParticipant.objects.create(
            tournament=tournament,
            user=request.user
        )
        messages.success(request, f'Вы присоединились к турниру "{tournament.title}"!')
    
    return redirect('tournaments:tournament_detail', tournament_id=tournament.id)