from django.urls import path, re_path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from tasks.api_views import TaskCategoryViewSet
urlpatterns = [
    path('notes/', include('note.api_urls')),
    path('users/', include('users.api_urls')),
    path('history/', include('history.api_urls')),
    path('friends/', include('friends.api_urls')),
    path('duels/', include('duels.api_urls')),
    path('shop/', include('shop.api_urls')),
    path('main/', include('main.api_urls')),
    # Tasks categories alias: /api/tasks/tasks/categories/ -> this handles it
    path('tasks/tasks/categories/', TaskCategoryViewSet.as_view({'get': 'list'}), name='tasks-categories-alias'),
    path('tasks/', include('tasks.api_urls')),
    path('tournaments/', include('tournaments.api_urls')),
    # Authentication: Djoser + SimpleJWT (all under auth/)
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]