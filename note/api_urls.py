from rest_framework.routers import DefaultRouter
from .api_views import NoteViewSet, NoteCategoryViewSet

router = DefaultRouter()
router.register(r'notes', NoteViewSet, basename='note')
router.register(r'categories', NoteCategoryViewSet, basename='category')



urlpatterns = router.urls
