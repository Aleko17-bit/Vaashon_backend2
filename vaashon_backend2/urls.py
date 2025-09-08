from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),        # Admin panel
    path('', include('shop.urls')),         # Frontend/auth routes
    path('api/', include('shop.api_urls')), # API routes (JSON)
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
