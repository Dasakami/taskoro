from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .models import FriendRequest, Friendship, FriendActivity

@login_required
def friend_list(request):
    # Get all friendships
    friendships = Friendship.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    )
    
    # Extract friend users
    friends = []
    for friendship in friendships:
        friend = friendship.user2 if friendship.user1 == request.user else friendship.user1
        friends.append(friend)
    
    # Get friend activities
    activities = FriendActivity.objects.filter(
        user__in=friends
    ).order_by('-created_at')[:10]
    
    context = {
        'friends': friends,
        'activities': activities,
    }
    
    return render(request, 'friends/friend_list.html', context)

@login_required
def search_users(request):
    query = request.GET.get('q', '')
    
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | 
            Q(profile__title__icontains=query)
        ).exclude(id=request.user.id)[:10]
    else:
        users = []
    
    # Get existing friendship statuses
    friend_requests = FriendRequest.objects.filter(
        (Q(sender=request.user) | Q(receiver=request.user)) &
        Q(status='pending')
    )
    
    context = {
        'users': users,
        'friend_requests': friend_requests,
        'query': query,
    }
    
    return render(request, 'friends/search_users.html', context)

@login_required
def friend_requests(request):
    received_requests = FriendRequest.objects.filter(
        receiver=request.user,
        status='pending'
    )
    
    sent_requests = FriendRequest.objects.filter(
        sender=request.user,
        status='pending'
    )
    
    context = {
        'received_requests': received_requests,
        'sent_requests': sent_requests,
    }
    
    return render(request, 'friends/friend_requests.html', context)

@login_required
def send_friend_request(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    
    # Check if already friends
    if Friendship.are_friends(request.user, receiver):
        messages.info(request, 'Вы уже являетесь друзьями.')
        return redirect('friends:friends')
    
    # Check for existing requests
    if FriendRequest.objects.filter(
        (Q(sender=request.user, receiver=receiver) |
         Q(sender=receiver, receiver=request.user)),
        status='pending'
    ).exists():
        messages.info(request, 'Запрос в друзья уже отправлен.')
        return redirect('friends:friends')
    
    FriendRequest.objects.create(sender=request.user, receiver=receiver)
    messages.success(request, f'Запрос в друзья отправлен {receiver.username}!')
    return redirect('friends:search_users')

@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(
        FriendRequest,
        id=request_id,
        receiver=request.user,
        status='pending'
    )
    
    friend_request.accept()
    messages.success(request, f'{friend_request.sender.username} добавлен в друзья!')
    return redirect('friends:friend_requests')

@login_required
def decline_friend_request(request, request_id):
    friend_request = get_object_or_404(
        FriendRequest,
        id=request_id,
        receiver=request.user,
        status='pending'
    )
    
    friend_request.decline()
    messages.info(request, 'Запрос в друзья отклонен.')
    return redirect('friends:friend_requests')

@login_required
def remove_friend(request, friend_id):
    friend = get_object_or_404(User, id=friend_id)
    
    Friendship.objects.filter(
        (Q(user1=request.user, user2=friend) |
         Q(user1=friend, user2=request.user))
    ).delete()
    
    messages.info(request, f'{friend.username} удален из друзей.')
    return redirect('friends:friends')
