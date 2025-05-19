from django.urls import path
from . import views
app_name = 'history'
urlpatterns = [
    path('', views.activity_log, name='history'),
    path('achievements/', views.achievement_list, name='achievements'),
]
