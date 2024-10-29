from django.urls import path
from project_mgmt import views

urlpatterns = [
    path('project_mgmt/projects', views.projectApi),
    path('project_mgmt/base/statuses', views.projectStatusApi),
    path('project_mgmt/base/types', views.projectTypesApi),
    path('project_mgmt/base/managers', views.managerApi),
    path('project_mgmt/base/calendars', views.projectCalendarsApi),
] 
