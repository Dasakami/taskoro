from django.contrib import admin
from django.urls import path,include, re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls import handler404, handler500, handler403,  handler400
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from main.views import base_template

handler404 = 'main.views.page_not_found'
handler500 = 'main.views.server_error'
handler403 = 'main.views.permission_denied'
handler400 = 'main.views.bad_request'

schema_view = get_schema_view(
   openapi.Info(
      title="My API",
      default_version='v1',
      description="Документация к API",
   ),
   public=False,
   permission_classes=(permissions.IsAdminUser,),
)

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),  
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}), 
    path('disko/', admin.site.urls),
   path('api/', include('sim.api_urls')),
   path('', base_template),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
