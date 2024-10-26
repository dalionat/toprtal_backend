from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MySubSystems, MyProfile, MyDepUsers



router = DefaultRouter()
router.register("subsystems", MySubSystems, basename="subsystems")
router.register(r'subsystems/(?P<pid>\d+)', MySubSystems)
router.register("profiles", MyProfile, basename="profiles")
router.register("depusers", MyDepUsers, basename="depusers")
router.register(r'depusers/(?P<did>\d+)', MyDepUsers)


urlpatterns = [
    path('', include(router.urls))
]