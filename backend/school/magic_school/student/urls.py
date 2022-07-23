from django.urls import path,include
from django import views
from .views import (
    StudentViewSet,
    SubjectViewSet,
    MarkViewset,
    AvaregViews,
    HomeworkTeacherViewsSet,
    HomeworkStudentViewSet,
    DailyLessonsViewSit,
    RecognizeFace,
    StudentAttendance
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
# urlpatterns = router.urls

urlpatterns =[
    path("",include(router.urls)),
    path("who/",RecognizeFace.as_view()),
    path("student-attendance/<int:student_id>/",StudentAttendance)
    ]

