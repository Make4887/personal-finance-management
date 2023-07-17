"""
URL configuration for budjet project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include(('polls.urls', 'polls'), namespace='polls')),
    path('admin/', admin.site.urls),
    path('register/', include('polls.urls')),
    path('about/', include('polls.urls')),
    path('', include('polls.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
