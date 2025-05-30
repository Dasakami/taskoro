from rest_framework.routers import DefaultRouter
from .api_views import TaskViewSet, BaseTaskViewSet, BaseTaskCompletionViewSet, TaskCategoryViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'base-tasks', BaseTaskViewSet, basename='base-task')
router.register(r'base-task-completions', BaseTaskCompletionViewSet, basename='base-task-completion')
router.register(r'categories', TaskCategoryViewSet, basename='category')

urlpatterns = router.urls
