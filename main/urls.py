from django.urls import include,path
from django.views.generic import TemplateView
from .views import main, complete_mission, custom_upload_function,admin_rofl
urlpatterns  = [
    path('', main, name='main'),
    path('tasks/',include(('tasks.urls'), namespace='tasks')),
    path('tournaments/',include(('tournaments.urls'), namespace='tournaments')),
    path('users/',include(('users.urls'), namespace='users')),
    path('duels/',include(('duels.urls'), namespace='duels')),
    path('friends/',include(('friends.urls'), namespace='friends')),
    path('shop/',include(('shop.urls'), namespace='shop')),
    path('notebook/',include(('note.urls'), namespace='note')),
    path('history/',include(('history.urls'), namespace='history')),
    path('complete_mission/<int:mission_id>/', complete_mission, name='complete_mission'),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('ckeditor/upload/', custom_upload_function , name='ckeditor_upload'),
    path('admin/', admin_rofl, name='admin_rofl'),
    path('yandex_9a99c4bc5ddefd70.html', TemplateView.as_view(template_name='yandex_9a99c4bc5ddefd70.html'))
]