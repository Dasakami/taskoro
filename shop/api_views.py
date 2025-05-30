from rest_framework import viewsets
from .models import ShopItem, Purchase, Chest, ChestOpening, ActiveBoost
from .serializers import ShopItemSerializer, PurchaseSerializer, ChestSerializer, ChestOpeningSerializer, ActiveBoostSerializer

class ShopItemViewSet(viewsets.ModelViewSet):
    queryset = ShopItem.objects.all()
    serializer_class = ShopItemSerializer

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

class ChestViewSet(viewsets.ModelViewSet):
    queryset = Chest.objects.all()
    serializer_class = ChestSerializer

class ChestOpeningViewSet(viewsets.ModelViewSet):
    queryset = ChestOpening.objects.all()
    serializer_class = ChestOpeningSerializer

class ActiveBoostViewSet(viewsets.ModelViewSet):
    queryset = ActiveBoost.objects.all()
    serializer_class = ActiveBoostSerializer
