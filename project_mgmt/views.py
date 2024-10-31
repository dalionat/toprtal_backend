from django.shortcuts import render
from re import sub

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework import viewsets

# Create your views here.
from project_mgmt.models import Project, ProjectStatus, ProjectType, ProjectCalendar
from project_mgmt.serializers import ProjectSerializer, ProjectStatusSerializer, ProjectTypeSerializer, ManagerSerializer
from project_mgmt.serializers import ProjectCalendarSerializer, TaskSerializer
from dashboard_mgmt.models import UserProfile
from django.contrib.auth.models import User
from organization_mgmt.models import Department
from .models import ProjectStatus, ProjectType, ProjectCalendar, Task


@csrf_exempt
@permission_classes([IsAuthenticated])
def projectApi(request, id=0):
    if request.method == 'GET':
        projects = Project.objects.all()
        projects_serialaizer = ProjectSerializer(projects, many=True)
        return JsonResponse(projects_serialaizer.data, safe=False)

    elif request.method == 'POST':
        header_token = request.META.get('HTTP_AUTHORIZATION', None)
        if header_token is not None:
            try:
                token = sub('Token ', '', header_token)
                token_obj = Token.objects.get(key=token)
                curr_user = token_obj.user
            except Token.DoesNotExist:
                return JsonResponse("Project failed to save", safe=False)
        
        project_data = JSONParser().parse(request)
        dep = Department.objects.get(department_id=project_data["department"])
        status = ProjectStatus.objects.get(project_status_id=project_data["status"])
        type = ProjectType.objects.get(project_type_id=project_data["project_type"])
        calendar = ProjectCalendar.objects.get(project_calendar_id=project_data["calendar"])
        manager  = User.objects.get(id=project_data["manager"])
        created_by = curr_user
        updated_by = curr_user
        
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
        return JsonResponse("Project Saved", safe=False)

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
def taskApi(request, project_id):
    header_token = request.META.get('HTTP_AUTHORIZATION', None)
    if header_token is None:
        return JsonResponse("", safe=False)
    if request.method == 'GET':
        tasks = Task.objects.filter(project_id = project_id)
        task_serializer = TaskSerializer(tasks, many=True)
        return JsonResponse(task_serializer.data, safe=False)   
    
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