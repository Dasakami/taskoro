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
    username = serializers.CharField(source='user.username', required=False)
    medals = MedalSerializer(many=True, read_only=True)
    character_classes = CharacterClassSerializer(many=True, read_only=True)
    
    # Добавляем поля для совместимости с Flutter
    id = serializers.CharField(source='user.id', read_only=True)
    avatar_url = serializers.SerializerMethodField()
    
    # Поля экипированных предметов
    equipped_background = serializers.SerializerMethodField()
    equipped_avatar_frame_color = serializers.SerializerMethodField()
    equipped_title = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'username', 'avatar', 'avatar_url', 
            'level', 'experience', 'experience_needed', 'streak',
            'coins', 'gems', 'bio', 'title', 'theme_preference', 'character_classes',
            'created_at', 'updated_at', 'medals',
            'equipped_background', 'equipped_avatar_frame_color', 'equipped_title'
        ]
        read_only_fields = ['level', 'experience', 'experience_needed', 
                           'streak', 'coins', 'gems', 'medals', 'character_classes']

    def get_avatar_url(self, obj):
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None

    def get_equipped_background(self, obj):
        item = obj.get_equipped_background()
        if item and hasattr(item, 'image') and item.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(item.image.url)
            return item.image.url
        return None

    def get_equipped_avatar_frame_color(self, obj):
        item = obj.get_equipped_avatar_frame()
        return item.color if item and hasattr(item, 'color') else None

    def get_equipped_title(self, obj):
        item = obj.get_equipped_title()
        return item.name if item and hasattr(item, 'name') else None

    def update(self, instance, validated_data):
        # Обновляем username если указан
        user_data = validated_data.pop('user', {})
        if 'username' in user_data:
            instance.user.username = user_data['username']
            instance.user.save()
        
        # Обновляем остальные поля профиля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
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