# friends/urls.py

from django.urls import path
from .api_views import (
    FriendListAPIView,
    friend_requests_api,
    send_friend_request_api,
    accept_friend_request_api,
    decline_friend_request_api,
    cancel_friend_request_api,
    remove_friend_api,
)

urlpatterns = [
    path('',                    FriendListAPIView.as_view(),         name='friends_list'),
    path('requests/',           friend_requests_api,                 name='friend_requests'),
    path('request/send/<int:user_id>/',      send_friend_request_api,    name='send_friend_request'),
    path('request/accept/<int:request_id>/', accept_friend_request_api, name='accept_friend_request'),
    path('request/decline/<int:request_id>/',decline_friend_request_api,name='decline_friend_request'),
    path('request/cancel/<int:request_id>/', cancel_friend_request_api,  name='cancel_friend_request'),
    path('  friend/remove/<int:user_id>/',     remove_friend_api,           name='remove_friend'),
]
