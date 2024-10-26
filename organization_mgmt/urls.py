from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import MyDepartments



router = DefaultRouter()
router.register("departments", MyDepartments, basename="departments")
router.register(r'departments/(?P<did>\d+)', MyDepartments)

urlpatterns = [
    path('', include(router.urls))
]