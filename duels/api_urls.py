from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .api_views import DuelViewSet, DuelProgressViewSet

router = DefaultRouter()
router.register(r'duels', DuelViewSet, basename='duel')
router.register(r'duel-progress', DuelProgressViewSet, basename='duel-progress')

urlpatterns = [
    path('', include(router.urls)),
]
