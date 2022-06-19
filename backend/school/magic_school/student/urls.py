from django.urls import path
from django import views
from .views import (
    StudentViewSet,
    SubjectViewSet,
    MarkViewset,
    AvaregViews,
    HomeworkTeacherViewsSet,
    HomeworkStudentViewSet,
    DailyLessonsViewSit,
)
from rest_framework import routers

app_name = "student_api"

router = routers.DefaultRouter()
router.register("student", StudentViewSet)
router.register("subject",SubjectViewSet)
router.register("mark",MarkViewset)
router.register("Avareg",AvaregViews)
router.register("homeworkteacher",HomeworkTeacherViewsSet)
router.register("homeworkStudent",HomeworkStudentViewSet)
router.register("dailyLessones",DailyLessonsViewSit)
urlpatterns = router.urls

