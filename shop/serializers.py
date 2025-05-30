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

class ChestOpeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChestOpening
        fields = '__all__'

class ActiveBoostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveBoost
        fields = '__all__'
