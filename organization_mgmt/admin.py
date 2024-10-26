from django.contrib import admin

# Register your models here.
from .models import Department, Level

admin.site.register(Department)
admin.site.register(Level)