from django.urls import path
from .api_views import MainPageAPIView

urlpatterns = [
    path('', MainPageAPIView.as_view(), name='api-main-page'),
]
