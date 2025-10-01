from django.urls import path
from . import api_views  

urlpatterns = [
    path('activity-log/', api_views.activity_log_api, name='activity_log_api'),
    path('achievements/', api_views.achievement_list_api, name='achievement_list_api'),
]
