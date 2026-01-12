from django.contrib import admin
from .models import Profile , CharacterClass,Medal  
from django.contrib.auth import get_user_model

User = get_user_model()

admin.site.register(Profile)
admin.site.register(CharacterClass)
admin.site.register(Medal)
