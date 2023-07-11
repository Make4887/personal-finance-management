"""
URL configuration for budjet project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include(('polls.urls', 'polls'), namespace='polls')),
    path('admin/', admin.site.urls),
    path('register/', include('polls.urls')),
    path('about/', include('polls.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
