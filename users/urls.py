from django.urls import path
from . import views
from django.urls import include
from .views import create_superuser

app_name = 'users'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path("create-superuser/", create_superuser),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
     path('profile/', include(('users.urls_profile'), namespace='profile')),
]