from django.contrib import admin
from django.urls import path, include
from api import views
from sendit_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('super-admin/', admin.site.urls),
    path('', include('api.urls', namespace ='api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
