from rest_framework import serializers
from .models import ShopItem, Purchase, Chest, ChestOpening, ActiveBoost

class ShopItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopItem
        fields = '__all__'

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'

class ChestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chest
        fields = '__all__'

from rest_framework import serializers
from .models import ChestOpening, Chest
import random

class ChestOpeningSerializer(serializers.ModelSerializer):
    chest = serializers.PrimaryKeyRelatedField(queryset=Chest.objects.all())
    chest_name = serializers.CharField(source='chest.name', read_only=True)

    class Meta:
        model = ChestOpening
        fields = ['id', 'chest', 'chest_name', 'coins_reward', 'gems_reward']
        read_only_fields = ['coins_reward', 'gems_reward', 'chest_name']

    def create(self, validated_data):
        user = self.context['request'].user
        profile = user.profile
        chest = validated_data['chest']

        if profile.coins < chest.price_coins or profile.gems < chest.price_gems:
            raise serializers.ValidationError("Недостаточно средств")

        # Списываем стоимость
        profile.coins -= chest.price_coins
        profile.gems -= chest.price_gems

        # Генерируем награды
        coins_reward = random.randint(chest.min_coins_reward, chest.max_coins_reward)
        gems_reward = random.randint(chest.min_gems_reward, chest.max_gems_reward)

        # Начисляем награды
        profile.coins += coins_reward
        profile.gems += gems_reward
        profile.save()

        opening = ChestOpening.objects.create(
            user=user,
            chest=chest,
            coins_reward=coins_reward,
            gems_reward=gems_reward
        )

        return opening


class ActiveBoostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveBoost
        fields = '__all__'
