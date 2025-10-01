
from django.urls import path
from .api_views import RegisterAPIView, LoginAPIView, UserProfileAPIView, UpdateProfileAPIView, UserSearchAPIView, \
    CharacterClassListUpdateAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='api_register'),
    path('login/', LoginAPIView.as_view(), name='api_login'),
    path('me/', UserProfileAPIView.as_view(), name='api-profile'),
    path('me/edit/', UpdateProfileAPIView.as_view(), name='api-edit-profile'),
    path(
      'character-classes/',
      CharacterClassListUpdateAPIView.as_view(),
      name='character-classes-list-update'
    ),
    path('search/', UserSearchAPIView.as_view(), name='api-user-search'),
]

