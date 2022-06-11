
from .views import (
    ClassroomViewSet,
    FeedbackViewSet,
    HolidayViewSet,
    PostViewSet,
    ProfileViewSet,
    MessageViewSet,

)
from rest_framework import routers
from django.urls import path

app_name = "manager_api"

router = routers.DefaultRouter()
router.register("post", PostViewSet)
router.register("holiday", HolidayViewSet)
router.register("classroom", ClassroomViewSet)
router.register("profile", ProfileViewSet)
router.register("feedback", FeedbackViewSet)
router.register("message", MessageViewSet)

urlpatterns = router.urls

