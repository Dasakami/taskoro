from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .models import *
from users.models import Profile


def friend_list(request):
    if not request.user.is_authenticated:
        context = {
            'friends': [],
            'activities': [],
        }
        return render(request, 'friends/friend_list.html', context)
    
    friendships = Friendship.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    )
    
    friends = []
    for friendship in friendships:
        friend = friendship.user2 if friendship.user1 == request.user else friendship.user1
        friends.append(friend)
    
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
    
    # Получаем профиль пользователя, так как FriendRequest работает с Profile
    user_profile = request.user.profile

    friend_requests = FriendRequest.objects.filter(
        (Q(sender=user_profile) | Q(receiver=user_profile)) &
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
    user_profile = request.user.profile

    received_requests = FriendRequest.objects.filter(
        receiver=user_profile,
        status='pending'
    )
    
    sent_requests = FriendRequest.objects.filter(
        sender=user_profile,
        status='pending'
    )
    
    context = {
        'received_requests': received_requests,
        'sent_requests': sent_requests,
    }
    
    return render(request, 'friends/friend_requests.html', context)


@login_required
def send_friend_request(request, user_id):
    receiver_user = get_object_or_404(User, id=user_id)
    sender_user = request.user

    # Проверяем, что у пользователя есть профиль
    sender_profile = sender_user.profile
    receiver_profile = receiver_user.profile

    # Проверка дружбы по модели Friendship (через User)
    if Friendship.are_friends(sender_user, receiver_user):
        messages.info(request, 'Вы уже являетесь друзьями.')
        return redirect('friends:friends')
    
    # Проверка, нет ли уже активных заявок между профилями
    if FriendRequest.objects.filter(
        (Q(sender=sender_profile, receiver=receiver_profile) | 
         Q(sender=receiver_profile, receiver=sender_profile)),
        status='pending'
    ).exists():
        messages.info(request, 'Запрос в друзья уже отправлен.')
        return redirect('friends:friends')
    
    FriendRequest.objects.create(sender=sender_profile, receiver=receiver_profile)
    messages.success(request, f'Запрос в друзья отправлен {receiver_user.username}!')
    return redirect('friends:search_users')


@login_required
def accept_friend_request(request, request_id):
    user_profile = request.user.profile

    friend_request = get_object_or_404(
        FriendRequest,
        id=request_id,
        receiver=user_profile,
        status='pending'
    )
    
    friend_request.accept()
    messages.success(request, f'{friend_request.sender.user.username} добавлен в друзья!')
    return redirect('friends:friend_requests')


@login_required
def decline_friend_request(request, request_id):
    user_profile = request.user.profile

    friend_request = get_object_or_404(
        FriendRequest,
        id=request_id,
        receiver=user_profile,
        status='pending'
    )
    
    friend_request.decline()
    messages.info(request, 'Запрос в друзья отклонен.')
    return redirect('friends:friend_requests')


@login_required
def remove_friend(request, friend_id):
    friend_user = get_object_or_404(User, id=friend_id)

    Friendship.objects.filter(
        (Q(user1=request.user, user2=friend_user) |
         Q(user1=friend_user, user2=request.user))
    ).delete()
    
    messages.info(request, f'{friend_user.username} удален из друзей.')
    return redirect('friends:friends')



@login_required
def open_chat(request, user_id):
    current_user = request.user
    other_user = get_object_or_404(User, id=user_id)

    # Сортировка для уникальности (user1 < user2)
    user1, user2 = (current_user, other_user) if current_user.id < other_user.id else (other_user, current_user)

    chat_group, created = ChatGroup.objects.get_or_create(user1=user1, user2=user2)
    chatroom_name = chat_group.get_group_name()

    return redirect('friends:chat_room', room_name=chatroom_name)

@login_required
def chat_room(request, room_name):
    # Извлекаем ID пользователей из room_name
    user_id_1, user_id_2 = map(int, room_name.split('_')[-2:])
    user1 = min(user_id_1, user_id_2)
    user2 = max(user_id_1, user_id_2)

    chat_group = ChatGroup.objects.get(user1_id=user1, user2_id=user2)
    messages = chat_group.messages.order_by('timestamp')

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'username': request.user.username,
        'messages': messages
    })
