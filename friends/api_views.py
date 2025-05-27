from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from django.db.models import Q
from .models import FriendRequest, Friendship
from .serializers import FriendRequestSerializer, FriendshipSerializer

# Получить список друзей текущего пользователя с профилями
class FriendListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FriendshipSerializer

    def get_queryset(self):
        user = self.request.user
        return Friendship.objects.filter(Q(user1=user) | Q(user2=user))


# Получить список заявок в друзья (полученные и отправленные)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def friend_requests_api(request):
    user = request.user
    received = FriendRequest.objects.filter(receiver=user, status='pending')
    sent = FriendRequest.objects.filter(sender=user, status='pending')
    received_serializer = FriendRequestSerializer(received, many=True)
    sent_serializer = FriendRequestSerializer(sent, many=True)
    return Response({
        'received_requests': received_serializer.data,
        'sent_requests': sent_serializer.data,
    })


# Отправить заявку в друзья
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def send_friend_request_api(request, user_id):
    sender = request.user
    try:
        receiver = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'detail': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)

    if Friendship.are_friends(sender, receiver):
        return Response({'detail': 'Вы уже друзья'}, status=status.HTTP_400_BAD_REQUEST)

    if FriendRequest.objects.filter(
        Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender),
        status='pending'
    ).exists():
        return Response({'detail': 'Заявка уже отправлена или получена'}, status=status.HTTP_400_BAD_REQUEST)

    FriendRequest.objects.create(sender=sender, receiver=receiver)
    return Response({'detail': 'Заявка отправлена'}, status=status.HTTP_201_CREATED)


# Принять заявку
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def accept_friend_request_api(request, request_id):
    user = request.user
    try:
        friend_request = FriendRequest.objects.get(id=request_id, receiver=user, status='pending')
    except FriendRequest.DoesNotExist:
        return Response({'detail': 'Заявка не найдена'}, status=status.HTTP_404_NOT_FOUND)

    friend_request.accept()
    return Response({'detail': 'Заявка принята'}, status=status.HTTP_200_OK)


# Отклонить заявку
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def decline_friend_request_api(request, request_id):
    user = request.user
    try:
        friend_request = FriendRequest.objects.get(id=request_id, receiver=user, status='pending')
    except FriendRequest.DoesNotExist:
        return Response({'detail': 'Заявка не найдена'}, status=status.HTTP_404_NOT_FOUND)

    friend_request.decline()
    return Response({'detail': 'Заявка отклонена'}, status=status.HTTP_200_OK)


# Удалить друга
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def remove_friend_api(request, user_id):
    user = request.user
    try:
        friend = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'detail': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)

    deleted, _ = Friendship.objects.filter(
        Q(user1=user, user2=friend) | Q(user1=friend, user2=user)
    ).delete()

    if deleted:
        return Response({'detail': 'Друг удален'}, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'Друг не найден'}, status=status.HTTP_400_BAD_REQUEST)
