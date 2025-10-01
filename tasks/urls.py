from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.task_list, name='tasks'),
    path('create/', views.task_create, name='task_create'),
    path('<int:task_id>/', views.task_detail, name='task_detail'),
    path('<int:task_id>/edit/', views.task_edit, name='task_edit'),
    path('<int:task_id>/delete/', views.task_delete, name='task_delete'),
    path('<int:task_id>/complete/', views.task_complete, name='task_complete'),

    path('class-tasks/', views.class_tasks_list, name='class_tasks'),
    path('class-tasks/<int:task_id>/', views.class_task_detail, name='class_task_detail'),
    path('class-tasks/<int:task_id>/complete/', views.complete_class_task, name='complete_class_task'),
    path('class-tasks/completed/', views.class_task_completed, name='class_task_completed'),

    path('habits/', views.habits_list, name='habits_list'),
    path('habits/create/', views.habit_create, name='habit_create'),
    path('habits/<int:habit_id>/', views.habits_detail, name='habit_detail'),
    path('habits/<int:habit_id>/complete/', views.habit_complete, name='habit_complete'),


    path('daily-goals/', views.daily_goals, name='daily_goals'),
    path('daily-goals/create/', views.daily_create, name='daily_create'),

    path('categories/', views.category_list, name='categories'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:category_id>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:category_id>/delete/', views.category_delete, name='category_delete'),
]
