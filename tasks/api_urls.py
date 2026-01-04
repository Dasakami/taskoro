from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .api_views import TaskViewSet, BaseTaskViewSet, BaseTaskCompletionViewSet, TaskCategoryViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'base-tasks', BaseTaskViewSet, basename='base-task')
router.register(r'base-task-completions', BaseTaskCompletionViewSet, basename='base-task-completion')
router.register(r'categories', TaskCategoryViewSet, basename='category')

urlpatterns = [
	path('', include(router.urls)),
	# Alias to support legacy Flutter calls to /tasks/tasks/categories/
	path('tasks/categories/', TaskCategoryViewSet.as_view({'get': 'list'}), name='task-categories-list-alias'),
]
