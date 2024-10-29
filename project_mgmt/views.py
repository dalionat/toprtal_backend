from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework import viewsets

# Create your views here.
from project_mgmt.models import Project, ProjectStatus, ProjectType, ProjectCalendar
from project_mgmt.serializers import ProjectSerializer, ProjectStatusSerializer, ProjectTypeSerializer, ManagerSerializer
from project_mgmt.serializers import ProjectCalendarSerializer
from dashboard_mgmt.models import UserProfile
from django.contrib.auth.models import User
from organization_mgmt.models import Department
from .models import ProjectStatus, ProjectType, ProjectCalendar


@csrf_exempt
def projectApi(request, id=0):
    if request.method == 'GET':
        projects = Project.objects.all()
        projects_serialaizer = ProjectSerializer(projects, many=True)
        return JsonResponse(projects_serialaizer.data, safe=False)

    elif request.method == 'POST':
        project_data = JSONParser().parse(request)
        
        dep = Department.objects.get(department_id=project_data["department"])
        status = ProjectStatus.objects.get(project_status_id=project_data["status"])
        type = ProjectType.objects.get(project_type_id=project_data["project_type"])
        calendar = ProjectCalendar.objects.get(project_calendar_id=project_data["calendar"])
        manager  = User.objects.get(id=project_data["manager"])
        created_by = User.objects.get(id=project_data["user"])
        updated_by = User.objects.get(id=project_data["user"])
        p = Project(title=project_data["title"],
                    description = project_data["description"],
                    department = dep,
                    project_type = type,
                    manager = manager,
                    created_by = created_by,
                    updated_by = updated_by,
                    status = status,
                    start_date = project_data["start_date"],
                    end_date = project_data["end_date"],
                    calendar = calendar)
        p.save()            
        
        
        # projects_serializer = ProjectSerializer(data=project_data)
        # if projects_serializer.is_valid():
        #     projects_serializer.save()
        #     return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed To create Project", safe=False)

    elif request.method == 'PUT':
        project_data = JSONParser().parse(request)
        project = Project.objects.get(ProjectId=project_data['ProjectId'])
        project_serializer = ProjectSerializer(project, data=project_data)

        if project_serializer.is_valid():
            project_serializer.save()
            return JsonResponse("updated Successfully", safe=False)
        return JsonResponse("Failed To update", safe=False)

    elif request.method == 'DELETE':
        project = Project.objects.get(ProjectId=id)
        project.delete()
        return JsonResponse("Deleted Successfully", safe=False)
    
@csrf_exempt
def projectStatusApi(request):
    if request.method == 'GET':
        statuses = ProjectStatus.objects.all()
        statuses_serialaizer = ProjectStatusSerializer(statuses, many=True)
        return JsonResponse(statuses_serialaizer.data, safe=False)
    
@csrf_exempt
def projectTypesApi(request):
    if request.method == 'GET':
        types = ProjectType.objects.all()
        types_serialaizer = ProjectTypeSerializer(types, many=True)
        return JsonResponse(types_serialaizer.data, safe=False)


@csrf_exempt
def managerApi(request):
    if request.method == 'GET':
        managers = UserProfile.objects.all()
        manager_serialaizer = ManagerSerializer(managers, many=True)
        return JsonResponse(manager_serialaizer.data, safe=False)


class Managers(viewsets.ModelViewSet):
    serializer_class = User
    queryset = User.objects.all()

    def get_queryset(self):
        curr_user = self.request.user
        userProfile = UserProfile.objects.get(user_id=curr_user)
        return self.queryset.filter(role_id = userProfile.user_id)
    
    
@csrf_exempt
def projectCalendarsApi(request, id=0):
    if request.method == 'GET':
        calendars = ProjectCalendar.objects.all()
        calendars_serialaizer = ProjectCalendarSerializer(calendars, many=True)
        return JsonResponse(calendars_serialaizer.data, safe=False)