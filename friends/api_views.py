from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import FriendRequest, Friendship
from .serializers import FriendRequestSerializer, FriendshipSerializer
from users.models import User

class FriendListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FriendshipSerializer

    def get_queryset(self):
        user = self.request.user
        return Friendship.objects.filter(Q(user1=user) | Q(user2=user))

    def get_serializer_context(self):
        return {'request': self.request}

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def friend_requests_api(request):
    user_profile = request.user.profile
    received = FriendRequest.objects.filter(receiver=user_profile, status='pending')
    sent = FriendRequest.objects.filter(sender=user_profile, status='pending')

    return Response({
        'received_requests': FriendRequestSerializer(received, many=True, context={'request': request}).data,
        'sent_requests': FriendRequestSerializer(sent, many=True, context={'request': request}).data,
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_friend_request_api(request, user_id):
    """
    Отправить запрос в друзья по ID пользователя
    """
    sender_user = request.user
    sender_profile = sender_user.profile

    try:
        receiver_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'detail': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)

    receiver_profile = receiver_user.profile

    # Проверка: не отправляет ли пользователь запрос самому себе
    if sender_user.id == receiver_user.id:
        return Response({'detail': 'Нельзя отправить запрос самому себе'}, status=status.HTTP_400_BAD_REQUEST)

    # Проверка: уже друзья?
    if Friendship.are_friends(sender_user, receiver_user):
        return Response({'detail': 'Вы уже друзья'}, status=status.HTTP_400_BAD_REQUEST)

    # Проверка: запрос уже существует?
    if FriendRequest.objects.filter(
        Q(sender=sender_profile, receiver=receiver_profile) | Q(sender=receiver_profile, receiver=sender_profile),
        status='pending'
    ).exists():
        return Response({'detail': 'Заявка уже существует'}, status=status.HTTP_400_BAD_REQUEST)

    # Создаем запрос
    FriendRequest.objects.create(sender=sender_profile, receiver=receiver_profile)
    return Response({'detail': 'Заявка отправлена'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_friend_request_by_body(request):
    """
    Accepts POST with JSON {'user_id': <id>} to be compatible with mobile client.
    ИСПРАВЛЕНО: извлекаем user_id и вызываем логику напрямую без передачи request.
    """
    user_id = request.data.get('user_id')
    if not user_id:
        return Response({'detail': 'user_id required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return Response({'detail': 'user_id must be integer'}, status=status.HTTP_400_BAD_REQUEST)

    # Вызываем ту же логику, что и в send_friend_request_api
    sender_user = request.user
    sender_profile = sender_user.profile

    try:
        receiver_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'detail': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)

    receiver_profile = receiver_user.profile

    if sender_user.id == receiver_user.id:
        return Response({'detail': 'Нельзя отправить запрос самому себе'}, status=status.HTTP_400_BAD_REQUEST)

    if Friendship.are_friends(sender_user, receiver_user):
        return Response({'detail': 'Вы уже друзья'}, status=status.HTTP_400_BAD_REQUEST)

    if FriendRequest.objects.filter(
        Q(sender=sender_profile, receiver=receiver_profile) | Q(sender=receiver_profile, receiver=sender_profile),
        status='pending'
    ).exists():
        return Response({'detail': 'Заявка уже существует'}, status=status.HTTP_400_BAD_REQUEST)

    FriendRequest.objects.create(sender=sender_profile, receiver=receiver_profile)
    return Response({'detail': 'Заявка отправлена'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def accept_friend_request_api(request, request_id):
    user_profile = request.user.profile
    fr = get_object_or_404(FriendRequest, id=request_id, receiver=user_profile, status='pending')
    fr.accept()
    return Response({'detail': 'Заявка принята'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def decline_friend_request_api(request, request_id):
    user_profile = request.user.profile
    fr = get_object_or_404(FriendRequest, id=request_id, receiver=user_profile, status='pending')
    fr.decline()
    return Response({'detail': 'Заявка отклонена'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def cancel_friend_request_api(request, request_id):
    user_profile = request.user.profile
    fr = get_object_or_404(FriendRequest, id=request_id, sender=user_profile, status='pending')
    fr.delete()
    return Response({'detail': 'Заявка отменена'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def remove_friend_api(request, user_id):
    friend_user = get_object_or_404(User, id=user_id)
    deleted, _ = Friendship.objects.filter(
        Q(user1=request.user, user2=friend_user) |
        Q(user1=friend_user, user2=request.user)
    ).delete()
    if deleted:
        return Response({'detail': 'Друг удалён'}, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'Друг не найден'}, status=status.HTTP_400_BAD_REQUEST)