from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Duel, DuelProgress
from friends.models import Friendship
from django.contrib.auth.models import User
from tasks.models import Task
from django.db import models
from friends.utils import get_friends

def duel_list(request):
    if not request.user.is_authenticated:
        context = {
            'active_duels': [],
            'pending_duels': [],
            'completed_duels': [],
        }
        return render(request, 'duels/duel_list.html', context)

    active_duels = Duel.objects.filter(
        models.Q(challenger=request.user) | models.Q(opponent=request.user),
        status='active'
    ).order_by('-created_at')

    pending_duels = Duel.objects.filter(
        opponent=request.user,
        status='pending'
    ).order_by('-created_at')

    completed_duels = Duel.objects.filter(
        models.Q(challenger=request.user) | models.Q(opponent=request.user),
        status='completed'
    ).order_by('-created_at')[:5]

    context = {
        'active_duels': active_duels,
        'pending_duels': pending_duels,
        'completed_duels': completed_duels,
    }

    return render(request, 'duels/duel_list.html', context)


@login_required
def create_duel(request, opponent_id):
    opponent = get_object_or_404(User, id=opponent_id)
    
    if not Friendship.are_friends(request.user, opponent):
        messages.error(request, 'Вы можете вызывать на дуэль только друзей.')
        return redirect('friends')
    
    if request.method == 'POST':
        task_id = request.POST.get('task')
        coins_stake = int(request.POST.get('coins_stake', 0))
        
        if coins_stake > request.user.profile.coins:
            messages.error(request, 'У вас недостаточно монет для такой ставки.')
            return redirect('friends')
        
        duel = Duel.objects.create(
            challenger=request.user,
            opponent=opponent,
            task_id=task_id,
            coins_stake=coins_stake
        )
        
        if coins_stake > 0:
            request.user.profile.coins -= coins_stake
            request.user.profile.save()
        
        messages.success(request, f'Вызов на дуэль отправлен {opponent.username}!')
        return redirect('duels:duel_detail', duel_id=duel.id)
    

    tasks = Task.objects.filter(user=request.user, is_completed=False)
    
    context = {
        'opponent': opponent,
        'tasks': tasks,
    }
    
    return render(request, 'duels/create_duel.html', context)

@login_required
def duel_detail(request, duel_id):
    duel = get_object_or_404(
        Duel.objects.filter(
            models.Q(challenger=request.user) | models.Q(opponent=request.user),
            id=duel_id
        )
    )
    
    context = {
        'duel': duel,
        'user_progress': duel.progress.filter(user=request.user).first(),
    }
    
    return render(request, 'duels/duel_detail.html', context)

@login_required
def accept_duel(request, duel_id):
    duel = get_object_or_404(Duel, id=duel_id, opponent=request.user, status='pending')

    if duel.coins_stake > request.user.profile.coins:
        messages.error(request, 'У вас недостаточно монет для принятия дуэли.')
        duel.decline_duel()
        return redirect('duels:duels')
    
    if duel.coins_stake > 0:
        request.user.profile.coins -= duel.coins_stake
        request.user.profile.save()
    
    duel.start_duel()
    
    DuelProgress.objects.create(duel=duel, user=duel.challenger)
    DuelProgress.objects.create(duel=duel, user=duel.opponent)
    
    messages.success(request, 'Дуэль началась! Приступайте к выполнению задания.')
    return redirect('duels:duel_detail', duel_id=duel.id)

@login_required
def decline_duel(request, duel_id):
    duel = get_object_or_404(Duel, id=duel_id, opponent=request.user, status='pending')
    duel.decline_duel()
    messages.info(request, 'Вы отклонили вызов на дуэль.')
    return redirect('duels:duels')

@login_required
def complete_duel_task(request, duel_id):
    duel = get_object_or_404(
        Duel.objects.filter(
            models.Q(challenger=request.user) | models.Q(opponent=request.user),
            id=duel_id,
            status='active'
        )
    )
    
    progress = get_object_or_404(DuelProgress, duel=duel, user=request.user)
    progress.complete_task()
    
    messages.success(request, 'Задание выполнено! Ожидаем результат противника.')
    return redirect('duels:duel_detail', duel_id=duel.id)



@login_required
def choose_opponent(request):
    friends = get_friends(request.user)
    return render(request, 'duels/choose_opponent.html', {'friends': friends})
