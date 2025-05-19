from django.contrib.auth.models import User
from .models import Friendship
from django.db.models import Q

def get_friends(user):
    friendships = Friendship.objects.filter(
        Q(user1=user) | Q(user2=user)
    )
    friend_ids = []
    for fs in friendships:
        friend_ids.append(fs.user2.id if fs.user1 == user else fs.user1.id)
    return User.objects.filter(id__in=friend_ids)
