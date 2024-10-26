from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework import viewsets

# Create your views here.
from project_mgmt.models import Project, ProjectStatus, ProjectType
from project_mgmt.serializers import ProjectSerializer, ProjectStatusSerializer, ProjectTypeSerializer, ManagerSerializer
from dashboard_mgmt.models import UserProfile
from django.contrib.auth.models import User


@csrf_exempt
def projectApi(request, id=0):
    if request.method == 'GET':
        projects = Project.objects.all()
        projects_serialaizer = ProjectSerializer(projects, many=True)
        return JsonResponse(projects_serialaizer.data, safe=False)

    elif request.method == 'POST':
        projec_data = JSONParser().parse(request)
        projects_serializer = ProjectSerializer(data=projec_data)

        if projects_serializer.is_valid():
            projects_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
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
def projectStatusApi(request, id=0):
    if request.method == 'GET':
        statuses = ProjectStatus.objects.all()
        statuses_serialaizer = ProjectStatusSerializer(statuses, many=True)
        return JsonResponse(statuses_serialaizer.data, safe=False)
    
@csrf_exempt
def projectTypesApi(request, id=0):
    if request.method == 'GET':
        types = ProjectType.objects.all()
        types_serialaizer = ProjectTypeSerializer(types, many=True)
        return JsonResponse(types_serialaizer.data, safe=False)


@csrf_exempt
def managerApi(request, id=0):
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