from django.db import models
from django.contrib.auth.models import User
from organization_mgmt.models import Department




class SubSystem(models.Model):
    subsystem_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    fa_title = models.CharField(max_length=100, blank=True)
    descritption = models.TextField(blank=True)
    url = models.CharField(max_length=25, blank=True)

    def __str__(self) -> str:
        return self.title
    
class Module(models.Model):
    module_id = models.AutoField(primary_key=True)
    subsystem_id = models.ForeignKey(SubSystem, to_field="subsystem_id", on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    fa_title = models.CharField(max_length=100)
    description = models.TextField(blank=True)


    def __str__(self) -> str:
        return self.title   

class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    level = models.SmallIntegerField()
    title = models.CharField(max_length=100)
    descritption = models.TextField(blank=True)
    subsystems = models.ManyToManyField(SubSystem)
    modules = models.ManyToManyField(Module)

    def __str__(self) -> str:
        return self.title

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING, blank=True, null=True)
    
    def __str__(self):
        return self.user.first_name + ' ' +  self.user.last_name + ' ' + self.department.title 
    
    
