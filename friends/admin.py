from django.contrib import admin
from .models import ChatGroup, Message, FriendActivity, FriendRequest, Friendship

admin.site.register(ChatGroup)
admin.site.register(Message)
admin.site.register(FriendRequest)
admin.site.register(FriendActivity)
admin.site.register(Friendship)