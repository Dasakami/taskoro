from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

from .models import Profile, Medal, CharacterClass

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    # Добавляем своё write_only-поле
    class_id = serializers.IntegerField(write_only=True)

    class Meta(UserCreateSerializer.Meta):
        model = User
        # Берём все стандартные поля Djoser + class_id
        fields = tuple(UserCreateSerializer.Meta.fields) + ('class_id',)

    def validate(self, attrs):
        # Забираем class_id до передачи в super().validate
        self._class_id = attrs.pop('class_id', None)
        return super().validate(attrs)

    def create(self, validated_data):
        # Создаём User через Djoser
        user = super().create(validated_data)

        # Гарантируем, что профиль существует
        profile, _ = Profile.objects.get_or_create(user=user)

        # Привязываем выбранный класс
        if getattr(self, '_class_id', None) is not None:
            try:
                cls = CharacterClass.objects.get(pk=self._class_id)
                # если у вас M2M
                profile.character_classes.add(cls)
                # если FK вместо M2M — 
                # profile.character_class = cls
                # profile.save()
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
    user = serializers.StringRelatedField()
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
