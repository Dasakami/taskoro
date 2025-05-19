from django.urls import path
from . import views
app_name = 'profile'
urlpatterns = [
    path('', views.profile_view, name='profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('<str:username>/', views.view_other_profile, name='view_other_profile'),
]