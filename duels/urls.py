
from django.urls import path
from . import views
app_name = 'duels'
urlpatterns = [
    path('', views.duel_list, name='duels'),
    path('create/<int:opponent_id>/', views.create_duel, name='create_duel'),
    path('<int:duel_id>/', views.duel_detail, name='duel_detail'),
    path('<int:duel_id>/accept/', views.accept_duel, name='accept_duel'),
    path('<int:duel_id>/decline/', views.decline_duel, name='decline_duel'),
    path('<int:duel_id>/complete/', views.complete_duel_task, name='complete_duel_task'),
    path('create/', views.choose_opponent, name='choose_opponent'),
]
