from django.contrib import admin
from django.urls import path

from django.conf.urls import include

urlpatterns = [
       path('admin/', admin.site.urls),
       path('api/', include('project_mgmt.urls')),
       path('api/v1/', include('djoser.urls')),
       path('api/v1/', include('djoser.urls.authtoken')),
       path('api/v1/', include('dashboard_mgmt.urls')),
       path('api/v1/', include('organization_mgmt.urls')),
]