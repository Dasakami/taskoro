from django.urls import path, re_path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
urlpatterns = [
        path('notes/', include('note.api_urls')),
    path('users/', include('users.api_urls')),
    path('history/', include('history.api_urls')),
    path('friends/', include('friends.api_urls')),
    path('duels/', include('duels.api_urls')),
    path('shop/', include('shop.api_urls')),
    path('main/', include('main.api_urls')),
    path('tasks/', include('tasks.api_urls')),
    path('tournaments/', include('tournaments.api_urls')),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]