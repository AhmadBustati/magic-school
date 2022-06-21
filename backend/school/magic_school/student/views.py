from cProfile import Profile
from telnetlib import STATUS
from unicodedata import name
# from matplotlib.style import context
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from yaml import serialize
from .models import Classroom, HomeWorkStudent,Profile
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
                            AverageSerializer,
                            
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
from rest_framework import status
from django.db.models import Avg, Max, Min, Sum


class StudentViewSet(ModelViewSet, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    def get_serializer_context(self):
        return {"student":self.request.GET.get('student')}

    def get_queryset(self):
        queryset=super(StudentViewSet,self).get_queryset()
        if self.request.GET.get('student'):
            return queryset.filter(id=self.request.GET.get('student'))
        return queryset
    
    
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
    ########## get query set using /?student=id###############
    # def get_queryset(self):
    #     queryset=super(MarkViewset,self).get_queryset()
    #     if self.request.GET.get('student'):
    #         return queryset.filter(student=self.request.GET.get('student'))
    #     return queryset 
    ########### get query set authentication ###############  
    def get_queryset(self):
        user=self.request.user  
        stu=Student.objects.get(user_id=user)
        return Mark.objects.filter(student_id=stu.id)

 


class AvaregViews(ModelViewSet,GeneratorExit):
    permission_classes = [IsAuthenticated]
    queryset=Mark.objects.all()
    serializer_class =AverageSerializer
    

    def get_serializer_context(self):
        return {"student":self.request.GET.get('student'),"subject":self.request.GET.get('subject') }


    def get_queryset(self):
        queryset=super(AvaregViews,self).get_queryset()
        if self.request.GET.get('student') and self.request.GET.get('subject'):
            queryset=queryset.filter(student=self.request.GET.get('student'),
                                        subject=self.request.GET.get('subject'),
                                        )
            #.aggregate(avge=(Sum("mark")/Sum("fullmark"))*100).get("avge",0.00)                            
            return  queryset      
        return  queryset  
               
                          
class HomeworkTeacherViewsSet(ModelViewSet,GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = HomeWorkeTeacherSerializer 
    queryset=HomeworkTeacher.objects.all()
########################  to save with authentication user #######################
    def perform_create(self, serializer):
        user=self.request.user  
        instance = serializer.save(teacher=Profile.objects.get(user_id=user.id))
########################  to get with teacher id  && /?classroom= #######################
    # def get_queryset(self):
    #     queryset=super(HomeworkTeacherViewsSet,self).get_queryset()
    #     if self.request.GET.get("teacher"):
    #         return queryset.filter(teacher=self.request.GET.get("teacher"))
    #     elif self.request.GET.get("classroom"):
    #        return queryset.filter(classroom=self.request.GET.get("classroom"))
    #     return queryset 
########################  to get with authentication user && /?classroom= #######################
    def get_queryset(self):
        queryset=super(HomeworkTeacherViewsSet,self).get_queryset()
        if self.request.GET.get("classroom"):
            return queryset.filter(classroom=self.request.GET.get("classroom"))
        else :
            user=self.request.user  
            return HomeworkTeacher.objects.filter(teacher=Profile.objects.get(user_id=user.id))




class HomeworkStudentViewSet(ModelViewSet,GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class=HomeWorkeStudentSerializer               
    queryset=HomeWorkStudent.objects.all()
    
    ########################  to save with authentication user #######################
    # def perform_create(self, serializer):
    #     user=self.request.user  
    #     instance = serializer.save(student=Student.objects.get(user_id=user.id))

    def get_queryset(self):
        queryset=super(HomeworkStudentViewSet,self).get_queryset()
        if self.request.GET.get("homework"):
            return queryset.filter(homework=self.request.GET.get("homework"))
        return queryset 
        
     


class DailyLessonsViewSit(ModelViewSet,GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class=DailyLessonsSerializer
    queryset=DailyLessons.objects.all()
# هلأ أنا هون بدي بس الموظف هو يلي يكريت الجداول ماظبطت ما بعرف ليش؟؟؟؟
    def perform_create(self, serializer):
        user=self.request.user 
        if user.account_type=="Employee": 
            instance = serializer.save()

    # def get_queryset(self):
    #     queryset=super(DailyLessonsViewSit,self).get_queryset()
    #     if self.request.GET.get("className"):
    #         return queryset.filter(className=self.request.GET.get("className"))
    #     elif self.request.GET.get("teacher"):
    #         return queryset.filter(teacher=self.request.GET.get("teacher"))
    #     return queryset  
    # ############################### get program with user authentication ##############################     
    def get_queryset(self):
        user=self.request.user
        print("@@@@@@@@@@@@@@@@@",user)
        queryset=super(DailyLessonsViewSit,self).get_queryset()
        print("@@@@@@@@@@@@@@@@@",queryset)
        
        if user.account_type=="teacher":
            print("@@@@@@@@@@@@@@@@@",user.account_type)
            return queryset.filter(teacher=Profile.objects.get(user_id=user.id))
        elif  user.account_type=="student":
            print("@@@@@@@@@@@@@@@@@",user.account_type) 
            obj=Student.objects.get(user_id=user.id)
            print("@@@@@@@@@@@@@@@@@",obj)  
            return queryset.filter(className=obj.classroom)