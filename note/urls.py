from django.urls import path
from . import views
app_name = 'note'
urlpatterns = [
    path('', views.notes_list, name='notes_list'),
    path('create/', views.note_create, name='note_create'),
    path('<int:pk>/', views.note_detail, name='note_detail'),
    path('<int:pk>/edit/', views.note_edit, name='note_edit'),
    path('categories/create/', views.create_note_category, name='create_category'),
    path('categories/', views.category_list, name='category_list'),
]
