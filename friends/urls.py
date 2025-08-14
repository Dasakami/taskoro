
from django.urls import path
from . import views
app_name = 'friends'
urlpatterns = [
    path('', views.friend_list, name='friends'),
    path('search/', views.search_users, name='search_users'),
    path('requests/', views.friend_requests, name='friend_requests'),
    path('send_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('decline_request/<int:request_id>/', views.decline_friend_request, name='decline_friend_request'),
    path('remove/<int:friend_id>/', views.remove_friend, name='remove_friend'),
    path('chat/open/<int:user_id>/', views.open_chat, name='open_chat'),
    path('chat/room/<str:room_name>/', views.chat_room, name='chat_room'),
]
