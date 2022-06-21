
from .views import (
    ClassroomViewSet,
    FeedbackViewSet,
    HolidayViewSet,
    PostViewSet,
    ProfileViewSet,
    MessageViewSet,
    AdminNumber,
    StudentNumber,
    TeacherNumber,
)
from rest_framework import routers
from django.urls import path,include

app_name = "manager_api"

router = routers.DefaultRouter()
router.register("post", PostViewSet)
router.register("holiday", HolidayViewSet)
router.register("classroom", ClassroomViewSet)
router.register("profile", ProfileViewSet)
router.register("feedback", FeedbackViewSet)
router.register("message", MessageViewSet)

# urlpatterns = router.urls

urlpatterns =[
    path("",include(router.urls)),
    path("AdminNumber/",AdminNumber),
    path("StudentNumber/",StudentNumber),
    path("TeacherNumber/",TeacherNumber),
]
