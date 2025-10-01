from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    ShopItemViewSet, PurchaseViewSet,
    ActiveBoostViewSet, ChestViewSet,
    ChestOpeningViewSet
)

router = DefaultRouter()
router.register(r'items', ShopItemViewSet, basename='item')
router.register(r'purchases', PurchaseViewSet, basename='purchase')
router.register(r'boosts', ActiveBoostViewSet, basename='boost')
router.register(r'chests', ChestViewSet, basename='chest')
router.register(r'openings', ChestOpeningViewSet, basename='opening')

urlpatterns = [
    path('', include(router.urls)),
]
