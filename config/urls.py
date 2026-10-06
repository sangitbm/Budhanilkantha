"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/login/', LoginView.as_view(template_name='core/login.html'), name='login'),

    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('news/', include('news.urls')),
    path('gallery/', include('gallery.urls')),
    path('records/', include('records.urls')),
]

# Serve uploaded media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
