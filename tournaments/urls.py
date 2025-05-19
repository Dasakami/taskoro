from django.urls import path
from . import views
app_name = 'tournaments'
urlpatterns = [
    path('', views.tournament_list, name='tournaments'),
    path('<int:tournament_id>/', views.tournament_detail, name='tournament_detail'),
    path('<int:tournament_id>/join/', views.tournament_join, name='tournament_join'),
]