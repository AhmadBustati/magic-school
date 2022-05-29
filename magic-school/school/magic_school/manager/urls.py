
from .views import (
    ClassroomViewSet,
    FeedbackViewSet,
    HolidayViewSet,
    PostViewSet,
    ProfileViewSet,
)
from rest_framework import routers

app_name = "manager_api"

router = routers.DefaultRouter()
router.register("post", PostViewSet)
router.register("holiday", HolidayViewSet)
router.register("classroom", ClassroomViewSet)
router.register("profile", ProfileViewSet)
router.register("feedback", FeedbackViewSet)

urlpatterns = router.urls
