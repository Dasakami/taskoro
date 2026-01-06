from datetime import timedelta
import random
from django.utils import timezone
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ShopItem, Purchase, ActiveBoost, Chest, ChestOpening
from .serializers import (
    ShopItemSerializer, PurchaseSerializer, ActiveBoostSerializer,
    ChestSerializer, ChestOpeningSerializer
)
from history.models import ActivityLog

class ShopItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list: GET /api/shop/items/?category=<slug>
    retrieve: GET /api/shop/items/{id}/
    """
    queryset = ShopItem.objects.filter(is_available=True)
    serializer_class = ShopItemSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category=category)
        return qs.order_by('-created_at')


class PurchaseViewSet(viewsets.ModelViewSet):
    """
    list:   GET  /api/shop/purchases/
    create: POST /api/shop/purchases/         (body: { "item_id": 5 })
    retrieve/partial_update/destroy: not exposed
    equip:  POST /api/shop/purchases/{id}/equip/
    unequip:POST /api/shop/purchases/{id}/unequip/
    """
    serializer_class = PurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Purchase.objects.filter(user=self.request.user).select_related('item')

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'])
    def equip(self, request, pk=None):
        purchase = self.get_object()
        item = purchase.item
        user = request.user
        profile = user.profile

        from django.db import transaction
        with transaction.atomic():
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

        return Response({
            'status': 'equipped',
            'purchase': PurchaseSerializer(purchase, context={'request': request}).data
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unequip(self, request, pk=None):
        purchase = self.get_object()
        item = purchase.item
        user = request.user
        profile = user.profile

        purchase.is_equipped = False
        purchase.save()

        if item.category == 'title':
            profile.title = ''
            profile.save()

        return Response({
            'status': 'unequipped',
            'purchase': PurchaseSerializer(purchase, context={'request': request}).data
        }, status=status.HTTP_200_OK)


class ActiveBoostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list: GET /api/shop/boosts/   (only active)
    """
    serializer_class = ActiveBoostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ActiveBoost.objects.filter(
            user=self.request.user,
            expires_at__gt=timezone.now()
        ).select_related('boost_item')


class ChestViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list: GET /api/shop/chests/
    open: POST /api/shop/chests/{id}/open/
    """
    queryset = Chest.objects.all()
    serializer_class = ChestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def open(self, request, pk=None):
        """
        Открыть сундук
        POST /api/shop/chests/{chest_id}/open/
        """
        chest = self.get_object()
        user = request.user
        profile = user.profile

        # Проверка достаточности средств
        if profile.coins < chest.price_coins or profile.gems < chest.price_gems:
            return Response(
                {"detail": "Недостаточно средств."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Списание стоимости
        profile.coins -= chest.price_coins
        profile.gems -= chest.price_gems

        # Генерация наград
        coins_reward = random.randint(chest.min_coins_reward, chest.max_coins_reward)
        gems_reward = random.randint(chest.min_gems_reward, chest.max_gems_reward)
        
        # Начисление наград
        profile.coins += coins_reward
        profile.gems += gems_reward
        profile.save()

        # Создание записи об открытии
        opening = ChestOpening.objects.create(
            user=user,
            chest=chest,
            coins_reward=coins_reward,
            gems_reward=gems_reward
        )
        
        # Запись в историю активности
        ActivityLog.objects.create(
            user=user,
            activity_type='chest_open',
            description=f'Открыт сундук "{chest.name}"',
            coins_gained=coins_reward,
            gems_gained=gems_reward
        )

        return Response({
            "id": str(opening.id),
            "coins_reward": coins_reward,
            "gems_reward": gems_reward,
            "chest": ChestSerializer(chest).data,
            "opened_at": opening.opened_at.isoformat(),
            "opening": ChestOpeningSerializer(opening).data
        }, status=status.HTTP_200_OK)


class ChestOpeningViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list: GET /api/shop/openings/
    """
    serializer_class = ChestOpeningSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChestOpening.objects.filter(user=self.request.user).select_related('chest')