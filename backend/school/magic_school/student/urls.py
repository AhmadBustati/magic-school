
from .views import (
    StudentViewSet,
    SubjectViewSet,
    MarkViewset,
    AvaregViews,
)
from rest_framework import routers

app_name = "student_api"

router = routers.DefaultRouter()
router.register("student", StudentViewSet)
router.register("subject",SubjectViewSet)
router.register("mark",MarkViewset)
router.register("Avareg",AvaregViews)
urlpatterns = router.urls

