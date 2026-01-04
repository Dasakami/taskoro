from rest_framework import serializers
from .models import ShopItem, Purchase, ActiveBoost, Chest, ChestOpening

class ShopItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopItem
        fields = '__all__'
        read_only_fields = ('is_available', 'created_at')


class PurchaseSerializer(serializers.ModelSerializer):
    item = ShopItemSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=ShopItem.objects.filter(is_available=True),
        write_only=True,
        source='item'
    )

    class Meta:
        model = Purchase
        fields = (
            'id', 'item', 'item_id', 'quantity',
            'total_price', 'purchased_at', 'is_equipped'
        )
        read_only_fields = ('id', 'item', 'total_price', 'purchased_at', 'is_equipped')

    def validate(self, attrs):
        user = self.context['request'].user
        item = attrs['item']
        profile = user.profile
        quantity = attrs.get('quantity', 1)
        total_price = item.price * quantity

        if Purchase.objects.filter(user=user, item=item).exists() and item.category not in ['chest', 'boost']:
            raise serializers.ValidationError("Вы уже приобрели этот предмет.")
        if item.currency == 'coins' and profile.coins < total_price:
            raise serializers.ValidationError("Недостаточно монет.")
        if item.currency == 'gems' and profile.gems < total_price:
            raise serializers.ValidationError("Недостаточно кристаллов.")
        attrs['total_price'] = total_price
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        item = validated_data['item']
        profile = user.profile

        from django.db import transaction
        quantity = validated_data.get('quantity', 1)
        total_price = validated_data.get('total_price', item.price * quantity)

        with transaction.atomic():
            # Deduct funds
            if item.currency == 'coins':
                profile.coins -= total_price
            else:
                profile.gems -= total_price
            profile.save()

            purchase = Purchase.objects.create(
                user=user,
                item=item,
                total_price=total_price,
                quantity=quantity
            )

        if item.category in ['title', 'avatar_frame', 'background']:
            Purchase.objects.filter(
                user=user,
                item__category=item.category,
                is_equipped=True
            ).update(is_equipped=False)

            purchase.is_equipped = True
            purchase.save()

            if item.category == 'title':
                profile.title = item.title_text
                profile.save()

        return purchase


class ActiveBoostSerializer(serializers.ModelSerializer):
    boost_item = ShopItemSerializer(read_only=True)

    class Meta:
        model = ActiveBoost
        fields = ('id', 'boost_item', 'multiplier',
                  'activated_at', 'expires_at', 'is_active')


class ChestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chest
        fields = '__all__'


class ChestOpeningSerializer(serializers.ModelSerializer):
    chest = ChestSerializer(read_only=True)

    class Meta:
        model = ChestOpening
        fields = ('id', 'chest', 'coins_reward',
                  'gems_reward', 'opened_at')
        read_only_fields = fields
