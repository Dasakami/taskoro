from django.contrib import admin
from .models import *

admin.site.register(ChatGroup)
admin.site.register(Message)
# Register your models here.
admin.site.register(FriendRequest)
admin.site.register(FriendActivity)
admin.site.register(Friendship)