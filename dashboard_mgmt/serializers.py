from rest_framework import serializers
from .models import SubSystem, Role, Module, UserProfile
from django.contrib.auth.models import User


class SubSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSystem
        fields = (
            "subsystem_id",
            "title",
            "fa_title",
            "url"
        )

class ModuleSerializer(serializers.ModelSerializer):
    subsystem_name = serializers.CharField(source='subsystem_id.title')
    class Meta:
        model = Module
        fields = (
            "subsystem_id",
            "title",
            "fa_title",
            "subsystem_name"
        )

class RoleSerialzer(serializers.ModelSerializer):
    subsystems = SubSystemSerializer(read_only=True, many=True)
    modules = ModuleSerializer(read_only=True, many=True)
    class Meta:
        model = Role
        fields = (
            "role_id",
            "title",
            "subsystems",
            "modules",
        )

class UserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id')
    first_name = serializers.CharField(source='user.first_name') 
    last_name = serializers.CharField(source='user.last_name') 
    role_id = serializers.IntegerField(source='role.role_id')
    role_title = serializers.CharField(source='role.title') 
    department_id = serializers.IntegerField(source='department.department_id')
    department_title = serializers.CharField(source='department.title')

    class Meta:
        model = UserProfile
        fields = ("id","user_id", "first_name","last_name" ,"role_id","role_title","department_id","department_title")


class UserSerializer(serializers.ModelSerializer):
    userprofiles = UserProfileSerializer(read_only=True, many=True)
    class Meta:
        model = User
        fields = ("id", "username", "userprofiles")