
from django.urls import path
from .api_views import RegisterAPIView, LoginAPIView, UserProfileAPIView, UpdateProfileAPIView, UserSearchAPIView, \
    CharacterClassListUpdateAPIView
from .api_views import UserProfileByIdAPIView
from .api_views import LogoutAPIView


app_name = 'users'

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='api_register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('me/', UserProfileAPIView.as_view(), name='api-profile'),
    path('me/edit/', UpdateProfileAPIView.as_view(), name='api-edit-profile'),
    path('profiles/<int:user_id>/', UserProfileByIdAPIView.as_view(), name='api-profile-by-id'),
    # alias to match Flutter client which calls /users/users/<id>/
    path('users/<int:user_id>/', UserProfileByIdAPIView.as_view(), name='api-profile-by-id-alias'),
    path('logout/', LogoutAPIView.as_view(), name='api-logout'),
    path(
      'character-classes/',
      CharacterClassListUpdateAPIView.as_view(),
      name='character-classes-list-update'
    ),
    path('search/', UserSearchAPIView.as_view(), name='api-user-search'),
]

