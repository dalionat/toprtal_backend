
from rest_framework import viewsets
from .serializers import RoleSerialzer, UserProfileSerializer, UserSerializer
from .models import Role, UserProfile
from django.contrib.auth.models import User

# Create your views here.


class MySubSystems(viewsets.ModelViewSet):
    serializer_class = RoleSerialzer
    queryset = Role.objects.all()

    def get_queryset(self):
        pid = self.request.query_params.get('pid')
        print(pid)
        userProfile = UserProfile.objects.get(id=pid)
        return self.queryset.filter(role_id = userProfile.role_id)


class MyProfile(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def get_queryset(self):
        curr_user = self.request.user
        return self.queryset.filter(user_id=curr_user)


class MyDepUsers(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def get_queryset(self):
        did = self.request.query_params.get('did')
        return self.queryset.filter(department_id = did)