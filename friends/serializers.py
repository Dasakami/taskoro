from rest_framework import serializers
from users.serializers import ProfileSerializer
from .models import FriendRequest, Friendship

class FriendRequestSerializer(serializers.ModelSerializer):
    sender = ProfileSerializer(read_only=True)
    receiver = ProfileSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'status', 'created_at']

class FriendshipSerializer(serializers.ModelSerializer):
    # Для отображения друга — показываем профиль другого пользователя
    friend_profile = serializers.SerializerMethodField()

    class Meta:
        model = Friendship
        fields = ['id', 'friend_profile', 'created_at']

    def get_friend_profile(self, obj):
        request_user = self.context['request'].user
        # Другой пользователь в дружбе
        friend_user = obj.user2 if obj.user1 == request_user else obj.user1
        profile = friend_user.profile
        serializer = ProfileSerializer(profile, context=self.context)
        return serializer.data
