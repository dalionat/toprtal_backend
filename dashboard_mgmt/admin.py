from django.contrib import admin

# Register your models here.
from .models import SubSystem, Module, Role, UserProfile

admin.site.register(SubSystem)
admin.site.register(Module)
admin.site.register(Role)
admin.site.register(UserProfile)