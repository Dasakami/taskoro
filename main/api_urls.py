from django.urls import path
from .api_views import MainPageAPIView
from .views import create_roles

urlpatterns = [
    path('', MainPageAPIView.as_view(), name='api-main-page'),
    path('create',create_roles )
]
