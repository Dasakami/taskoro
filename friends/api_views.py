from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import FriendRequest, Friendship
from .serializers import FriendRequestSerializer, FriendshipSerializer
from users.models import User

# 2.1. Список друзей с профилями
class FriendListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FriendshipSerializer

    def get_queryset(self):
        user = self.request.user
        return Friendship.objects.filter(Q(user1=user) | Q(user2=user))

    def get_serializer_context(self):
        return {'request': self.request}

# 2.2. Список заявок
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

# 2.3. Отправка заявки
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_friend_request_api(request, user_id):
    sender_user = request.user
    sender_profile = sender_user.profile

    try:
        receiver_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'detail': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)

    receiver_profile = receiver_user.profile

    # Проверка, не являются ли они уже друзьями
    if Friendship.are_friends(sender_user, receiver_user):
        return Response({'detail': 'Вы уже друзья'}, status=status.HTTP_400_BAD_REQUEST)

    # Проверка, нет ли уже заявки между ними
    if FriendRequest.objects.filter(
        Q(sender=sender_profile, receiver=receiver_profile) | Q(sender=receiver_profile, receiver=sender_profile),
        status='pending'
    ).exists():
        return Response({'detail': 'Заявка уже существует'}, status=status.HTTP_400_BAD_REQUEST)

    FriendRequest.objects.create(sender=sender_profile, receiver=receiver_profile)
    return Response({'detail': 'Заявка отправлена'}, status=status.HTTP_201_CREATED)

# 2.4. Принять заявку
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def accept_friend_request_api(request, request_id):
    user_profile = request.user.profile
    fr = get_object_or_404(FriendRequest, id=request_id, receiver=user_profile, status='pending')
    fr.accept()
    return Response({'detail': 'Заявка принята'}, status=status.HTTP_200_OK)

# 2.5. Отклонить заявку
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def decline_friend_request_api(request, request_id):
    user_profile = request.user.profile
    fr = get_object_or_404(FriendRequest, id=request_id, receiver=user_profile, status='pending')
    fr.decline()
    return Response({'detail': 'Заявка отклонена'}, status=status.HTTP_200_OK)

# 2.6. Отменить исходящую заявку
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def cancel_friend_request_api(request, request_id):
    user_profile = request.user.profile
    fr = get_object_or_404(FriendRequest, id=request_id, sender=user_profile, status='pending')
    fr.delete()
    return Response({'detail': 'Заявка отменена'}, status=status.HTTP_204_NO_CONTENT)

# 2.7. Удалить друга
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
