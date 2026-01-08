"""
URL configuration for me_api project.

Routes:
- /admin/           -> Django admin
- /health           -> Health check endpoint
- /api/             -> All API endpoints
"""
from django.contrib import admin
from django.urls import path, include

from profiles.views import HealthCheckView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health', HealthCheckView.as_view(), name='health'),
    path('api/', include('profiles.urls')),
]

