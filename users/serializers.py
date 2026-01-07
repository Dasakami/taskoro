from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

from .models import Profile, Medal, CharacterClass

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class_id = serializers.IntegerField(write_only=True, required=True)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = tuple(UserCreateSerializer.Meta.fields) + ('class_id',)

    def validate_class_id(self, value):
        """Проверяем что класс существует"""
        try:
            CharacterClass.objects.get(pk=value)
        except CharacterClass.DoesNotExist:
            raise serializers.ValidationError('Класс персонажа не найден')
        return value

    def validate(self, attrs):
        # Сохраняем class_id перед вызовом родительского validate
        self._class_id = attrs.pop('class_id', None)
        
        # Проверяем что class_id передан
        if self._class_id is None:
            raise serializers.ValidationError({'class_id': 'Выберите класс персонажа'})
        
        return super().validate(attrs)

    def create(self, validated_data):
        # Создаем пользователя через родительский метод
        user = super().create(validated_data)

        # Создаем или получаем профиль
        profile, created = Profile.objects.get_or_create(user=user)

        # Добавляем класс персонажа
        if hasattr(self, '_class_id') and self._class_id is not None:
            try:
                character_class = CharacterClass.objects.get(pk=self._class_id)
                profile.character_classes.add(character_class)
                profile.save()
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
    avatar = serializers.ImageField(required=False, allow_null=True)
    
    # Добавляем id в serializer
    id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'username', 'avatar', 'level', 'experience', 'experience_needed', 
            'streak', 'coins', 'gems', 'bio', 'title', 'theme_preference', 
            'character_classes', 'created_at', 'updated_at', 'medals'
        ]
        read_only_fields = [
            'id', 'user', 'username', 'level', 'experience', 'experience_needed', 
            'streak', 'coins', 'gems', 'created_at', 'updated_at', 'medals'
        ]
    
    def get_id(self, obj):
        """Возвращаем ID пользователя, а не профиля"""
        return obj.user.id
    
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