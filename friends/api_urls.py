from django.urls import path
from .api_views import (
    FriendListAPIView,
    friend_requests_api,
    send_friend_request_api,
    send_friend_request_by_body,
    accept_friend_request_api,
    decline_friend_request_api,
    cancel_friend_request_api,
    remove_friend_api,
)

urlpatterns = [
    path('',                    FriendListAPIView.as_view(),         name='friends_list'),
    path('requests/',           friend_requests_api,                 name='friend_requests'),
    path('request/send/<int:user_id>/',      send_friend_request_api,    name='send_friend_request'),
    path('request/send/',                     send_friend_request_by_body, name='send_friend_request_body'),
    path('request/<int:request_id>/accept/', accept_friend_request_api, name='accept_friend_request'),
    path('request/<int:request_id>/decline/',decline_friend_request_api,name='decline_friend_request'),
    path('request/<int:request_id>/cancel/', cancel_friend_request_api,  name='cancel_friend_request'),
    path('friend/remove/<int:user_id>/',     remove_friend_api,           name='remove_friend'),
    # alias to match Flutter client which calls /friends/remove/<id>/
    path('remove/<int:user_id>/',            remove_friend_api,           name='remove_friend_alias'),
]
