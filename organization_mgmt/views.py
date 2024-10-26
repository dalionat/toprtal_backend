from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .serializers import DepartmentSerializer
from .models import Department
from django.db.models import Q
# Create your views here.


class MyDepartments(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()

    def get_queryset(self):
        did = self.request.query_params.get('did')
        return self.queryset.filter(Q(department_id = did) | Q(parent = did))