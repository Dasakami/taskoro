# users/serializers.py
from rest_framework import serializers
from .models import Profile, Medal, CharacterClass
from django.contrib.auth.models import User

class CharacterClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterClass
        fields = ['id', 'name', 'description', 'icon', 'color']

class MedalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medal
        fields = ['name', 'description', 'medal_type', 'acquired_date']

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # или user.username
    medals = MedalSerializer(many=True, read_only=True)
    character_classes = CharacterClassSerializer(many=True, read_only=True)
    
    class Meta:
        model = Profile
        fields = [
            'user', 'avatar', 'level', 'experience', 'experience_needed', 'streak',
            'coins', 'gems', 'bio', 'title', 'theme_preference', 'character_classes',
            'created_at', 'updated_at', 'medals'
        ]


class UserSearchSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'avatar_url']

    def get_avatar_url(self, obj):
        profile = getattr(obj, 'profile', None)
        if profile and profile.avatar:
            request = self.context.get('request')
            avatar_url = profile.avatar.url
            if request is not None:
                return request.build_absolute_uri(avatar_url)
            return avatar_url
        return None
    

class CompactUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class CompactProfileSerializer(serializers.ModelSerializer):
    user = CompactUserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'level']
