from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import include
app_name = 'users'
urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', include(('users.urls_profile'), namespace='profile')),
    
]