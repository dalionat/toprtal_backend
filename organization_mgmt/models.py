from django.db import models

# Create your models here.

class Level(models.Model):
    level_id = models.AutoField(primary_key=True)
    code = models.PositiveSmallIntegerField(unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.title
    
class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    code = models.PositiveSmallIntegerField(unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    parent = models.ForeignKey("Department", to_field="department_id",on_delete=models.CASCADE, blank=True, null=True)
    level = models.ForeignKey(Level,to_field="level_id" ,on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.title