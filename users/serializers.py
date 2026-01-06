from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

from .models import Profile, Medal, CharacterClass

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class_id = serializers.IntegerField(write_only=True)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = tuple(UserCreateSerializer.Meta.fields) + ('class_id',)

    def validate(self, attrs):
        self._class_id = attrs.pop('class_id', None)
        return super().validate(attrs)

    def create(self, validated_data):
        user = super().create(validated_data)

        profile, _ = Profile.objects.get_or_create(user=user)

        if getattr(self, '_class_id', None) is not None:
            try:
                cls = CharacterClass.objects.get(pk=self._class_id)
                profile.character_classes.add(cls)
            except CharacterClass.DoesNotExist:
                pass

        return user


class CharacterClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterClass
        fields = ['id', 'name', 'description', 'icon', 'color']


class MedalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medal
        fields = ['name', 'description', 'medal_type', 'acquired_date']


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    medals = MedalSerializer(many=True, read_only=True)
    character_classes = CharacterClassSerializer(many=True, read_only=True)
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = Profile
        fields = [
            'user', 'username', 'avatar', 'level', 'experience', 'experience_needed', 
            'streak', 'coins', 'gems', 'bio', 'title', 'theme_preference', 
            'character_classes', 'created_at', 'updated_at', 'medals'
        ]
        read_only_fields = [
            'user', 'username', 'level', 'experience', 'experience_needed', 
            'streak', 'coins', 'gems', 'created_at', 'updated_at', 'medals'
        ]
    
    def update(self, instance, validated_data):
        # Обновляем только разрешенные поля
        instance.bio = validated_data.get('bio', instance.bio)
        instance.theme_preference = validated_data.get('theme_preference', instance.theme_preference)
        
        # Обработка аватара
        if 'avatar' in validated_data:
            instance.avatar = validated_data['avatar']
        
        instance.save()
        return instance


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
            return request.build_absolute_uri(avatar_url) if request else avatar_url
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