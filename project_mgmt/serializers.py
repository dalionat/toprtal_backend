
from rest_framework import serializers
from .models import Project, ProjectStatus, ProjectType, ProjectCalendar
from .models import Task, CostType
from django.contrib.auth.models import User
from dashboard_mgmt.models import UserProfile


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')

class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = ('project_type_id', 'fa_title')

class ProjectSerializer(serializers.ModelSerializer):
    department_title = serializers.CharField(source='department.title')
    status_title = serializers.CharField(source='status.title')
    manager = ManagerSerializer(read_only=True, many=False)
    class Meta:
        model = Project
        fields = ('project_id', 
                  'title', 
                  'department_title', 
                  'manager',
                  'status_title',
                  'start_date',
                  'end_date',
                  )   
        
class ProjectStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectStatus
        fields = ('project_status_id', 'title')
        
        
class ProjectCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCalendar
        fields = ('project_calendar_id', 'title')
        
        
class AssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')
        
class CostTypeSerialaizer(serializers.ModelSerializer):
    class Meta:
        model = CostType 
        fields = ('cost_type_id', 'title', 'fa_title')
        
class ParentTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('task_id', 'title')
        
class TaskSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True, many=False)
    assigne = AssigneeSerializer(read_only=True, many=False)
    parent = ParentTaskSerializer(read_only=True, many=False)
    cost_type = CostTypeSerialaizer(read_only=True, many=False)
    
    class Meta:
        model = Task
        fields = (
            'task_id',
            'title',
            'project',
            'assigne',
            'parent',
            'is_summery',
            'weight',
            'start_date',
            'end_date',
            'cost_type',
            'cost',
            'actual_progress', 
        )