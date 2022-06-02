from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import Classroom, HomeWorkStudent
from .models import Student,Subject,Mark,HomeworkTeacher,DailyLessons
from django.http import Http404
from django.db.models import Q
from .serializers import (
                            StudentSerializer,
                            SubjectSerializer,
                            MarkSerializer,
                            HomeWorkeTeacherSerializer,
                            HomeWorkeStudentSerializer,
                            DailyLessonsSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db.models import Avg, Max, Min, Sum


class StudentViewSet(ModelViewSet, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if request.GET.get("classroom"):
            class_id = request.GET.get("classroom")
            
            try:
                classroom = Classroom.objects.get(pk=class_id)
                
            except Classroom.DoesNotExist:
                raise Http404("classroom does not exist")
            queryset = queryset.filter(classroom=classroom)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class SubjectViewSet(ModelViewSet,GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class MarkViewset(ModelViewSet,GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset=Mark.objects.all()
    serializer_class = MarkSerializer
    
    def get_queryset(self):
        queryset=super(MarkViewset,self).get_queryset()
        if self.request.GET.get('student'):
            return queryset.filter(student=self.request.GET.get('student'))
        return queryset   

        
class AvaregViews(ModelViewSet,GeneratorExit):
    permission_classes = [IsAuthenticated]
    serializer_class = MarkSerializer
    queryset=Mark.objects.all()
    def get_queryset(self):
        queryset=super(AvaregViews,self).get_queryset()
        if self.request.GET.get('student') and self.request.GET.get('subject'):
            # sum_mark=queryset.filter(student=self.request.GET.get('student'),subject=self.request.GET.get('subject')).aggregate(Sum("mark"))
            # print("***************************************",sum_mark)
            # sum_fullmark=queryset.filter(student=self.request.GET.get('student'),subject=self.request.GET.get('subject')).aggregate(Sum("fullmark"))
            # print("***************************************",sum_fullmark)
            # average_mark=(mark__sum/fullmark__sum)*100
            # print("***************************************",average_mark)
            return queryset.filter(student=self.request.GET.get('student'),subject=self.request.GET.get('subject'))          
        return  queryset  
               
                          
class HomeworkTeacherViewsSet(ModelViewSet,GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = HomeWorkeTeacherSerializer 
    queryset=HomeworkTeacher.objects.all()

    def get_queryset(self):
        queryset=super(HomeworkTeacherViewsSet,self).get_queryset()
        if self.request.GET.get("teacher"):
            return queryset.filter(teacher=self.request.GET.get("teacher"))
        return queryset 


class HomeworkStudentViewSet(ModelViewSet,GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class=HomeWorkeStudentSerializer               
    queryset=HomeWorkStudent.objects.all()

    def get_queryset(self):
        queryset=super(HomeworkStudentViewSet,self).get_queryset()
        if self.request.GET.get("homework"):
            return queryset.filter(homework=self.request.GET.get("homework"))
        return queryset 
        
     
class DailyLessonsViewSit(ModelViewSet,GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class=DailyLessonsSerializer
    queryset=DailyLessons.objects.all()
    def get_queryset(self):
        queryset=super(DailyLessonsViewSit,self).get_queryset()
        if self.request.GET.get("className"):
            return queryset.filter(className=self.request.GET.get("className"))
        elif self.request.GET.get("teacher"):
            return queryset.filter(teacher=self.request.GET.get("teacher"))
        return queryset       

