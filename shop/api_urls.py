from django.urls import path, include
from rest_framework.routers import DefaultRouter
from shop.api_views import ShopItemViewSet, PurchaseViewSet, ChestViewSet, ChestOpeningViewSet, ActiveBoostViewSet

router = DefaultRouter()
router.register(r'shop-items', ShopItemViewSet)
router.register(r'purchases', PurchaseViewSet)
router.register(r'chests', ChestViewSet)
router.register(r'chest-openings', ChestOpeningViewSet)
router.register(r'active-boosts', ActiveBoostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
