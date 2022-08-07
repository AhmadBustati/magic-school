from django.urls import path,include
from django import views
from .views import (
    StudentViewSet,
    SubjectViewSet,
    MarkViewset,
    HomeworkTeacherViewsSet,
    HomeworkStudentViewSet,
    DailyLessonsViewSit,
    RecognizeFace,
    AnswerView,
    StudentAttendanceStatus,
    ActivityViewSet,
    StudentAttendance,
    StudentAttendanceMonthly,
    AvaregViews,
    studentBirthday,
)
from rest_framework import routers

app_name = "student_api"

router = routers.DefaultRouter()
router.register("student", StudentViewSet)
router.register("subject",SubjectViewSet)
router.register("mark",MarkViewset)
router.register("homeworkteacher",HomeworkTeacherViewsSet)
router.register("homeworkStudent",HomeworkStudentViewSet)
router.register("dailyLessones",DailyLessonsViewSit)
router.register("Activity",ActivityViewSet)

# urlpatterns = router.urls

urlpatterns =[
    path("",include(router.urls)),
    path("who/",RecognizeFace.as_view()),
    path("Answer/",AnswerView.as_view()),
    path("Answer/<int:id>/",AnswerView.as_view()),
    path("student-absent/",StudentAttendanceStatus.as_view()),
    path("student-absent/<int:id>/",StudentAttendanceStatus.as_view()),
    path("student-attendance/<int:student_id>/",StudentAttendance),
    path("student-attendance-monthly/<int:student_id>/",StudentAttendanceMonthly),
    path("Avareg/<int:student_id>/",AvaregViews),
    path("birthday/<int:id>/",studentBirthday)
    ]

