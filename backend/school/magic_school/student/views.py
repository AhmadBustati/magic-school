from cProfile import Profile
import json
from telnetlib import STATUS
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.urls import is_valid_path 
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from yaml import serialize
from datetime import date
import numpy as np 

from manager.models import QuizName
from .models import  HomeWorkStudent,Profile,face_recognition,Attendance
from .models import Student,Subject,Mark,HomeworkTeacher,DailyLessons,Answer,Activity

from rest_framework import status

from manager.serializers import QuizSerializer

from .serializers import (
                            StudentSerializer,
                            StudentSerializerGET,
                            SubjectSerializer,
                            MarkSerializer,
                            HomeWorkeTeacherSerializer,
                            HomeWorkeStudentSerializer,
                            DailyLessonsSerializer,
                            AverageSerializer,
                            AttendanceSerializer,
                            MonthlyAttendance,
                            AnswerSerializer,
                            CountSerializer,
                            ActivitySerializer,
                            
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.http import HttpResponse, JsonResponse

def StudentAttendance(request,student_id):
    if  student_id:
        query = (Attendance.objects.filter(student=Student.objects.get(id=student_id))
        .values("attendance_status")
        .annotate(count=Count("attendance_status"))
        .order_by())
        response = CountSerializer(query,many=True)
        return JsonResponse(response.data,safe=False)

def StudentAttendanceMonthly(request,student_id):
    queryset = (Attendance.objects.filter(student=Student.objects.get(id=student_id))
            .annotate(month=TruncMonth("day"))
            .values("month")
            .annotate(count=Count("attendance_status"))
            .values("month","count","attendance_status")
            .order_by("month"))
    response_lst=[]
    response_json={"leave":0,"absent":0,"present":0}
    for query in queryset:
        a={}# A dictionary to update the list which is used to get over the pointers
        month = query["month"].strftime("%b")#Get the string of the month
        attendance_status = query["attendance_status"]# present,absent,or leave
        if "month" in response_json :
            if response_json["month"] ==month:
                response_json[attendance_status] = query["count"]

            else:
                a.update(response_json)# not to update the values in the list 
                response_lst.append(a)
                response_json["month"]=month
                response_json[attendance_status] = query["count"]

        
        else:
            response_json["month"]=month
            response_json[attendance_status] = query["count"]

    response_lst.append(response_json)
    
        


    # response = MonthlyAttendance(respons,many=True)
    return JsonResponse(response_lst,safe=False)




class StudentViewSet(ModelViewSet, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Student.objects.all()
    filter_backends=[SearchFilter]
    search_fields=["first_name","last_name"]
    
    def get_serializer_class(self):
        if self.action == 'list' :
            if self.request.GET.get('student'):
                return StudentSerializerGET     
        return StudentSerializer

    def get_serializer_context(self):
        return {"student":self.request.GET.get('student')}
    
    def get_queryset(self):
        queryset=super(StudentViewSet,self).get_queryset()
        if self.request.GET.get('student'):
            return queryset.filter(id=self.request.GET.get('student'))
        elif self.request.GET.get('classroom'):
            return queryset.filter(classroom=self.request.GET.get('classroom'))
        return queryset
    
    def update(self, request, *args, **kwargs):
        return super(StudentViewSet,self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(StudentViewSet,self).destroy(request, *args, **kwargs)   

    
            

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
    def get_queryset(self):
        queryset=super(DailyLessonsViewSit,self).get_queryset()
        if self.request.GET.get("className"):
            return queryset.filter(className=self.request.GET.get("className"))
        elif self.request.GET.get("teacher"):
            return queryset.filter(teacher=self.request.GET.get("teacher"))
        return queryset 
    def create(self,request,*arg,**Kwargs):
        item=request.data
        if isinstance(item,list):
            serialize=self.serializer_class(instance="",
                                            data=item,
                                            many=True,
                                            context={
                                                "request":self.request,
                                            }
                                            )
            if serialize.is_valid(raise_exception=True):
                serialize.save()
                return Response(serialize.data,status=status.HTTP_200_OK)
            return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)    
        elif isinstance(item,dict):
            return self.create(request,*arg,**Kwargs)


class RecognizeFace(APIView):
    def post(self,request):
        im = request.data.get('face')
        image = np.array(im)
        recognizer = face_recognition()
        queryset = Student.objects.all()
        id = recognizer.recognize_face(image,queryset)
        if id == "not recognized":
            return Response(id)
        student_attendance =Attendance(
            student=Student.objects.get(id=id),
            attendance_status="present")
        student_attendance.save()
        return Response(id)

class StudentAttendanceStatus(APIView):
    def get(self,request):
        query = Student.objects.exclude(id__in=Attendance.objects.filter(day=date.today()))
        for i in range(len(query)):
            student_attendance = Attendance(
                student=query[i]
            )
            student_attendance.save()

        return Response(len(query))

    def put(self,request,id):
        student=self.get_student(id)
        student.attendance_status="leave"
        student.save()
        return Response("success",status = status.HTTP_202_ACCEPTED)
        # serializer=AttendanceSerializer(student)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data,status=status.HTTP_200_OK)
        # return Response(status=status.HTTP_400_BAD_REQUEST)


    def get_student(self,id):
        try:
            return Attendance.objects.get(student=id)
        except:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    


class AnswerView(APIView):
    def get_object(self,id):
        try:
            return Answer.objects.get(id=id)
        except:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)


    def get (self,request,id=None):
        if self.request.GET.get("teacher_id"):
            response = QuizName.objects.filter(profile=self.request.GET.get("teacher_id"))
            serializer = QuizSerializer(response,many=True)
            return Response(serializer.data)

        elif self.request.GET.get("class_id"):
            response = QuizName.objects.filter(class_name=self.request.GET.get("class_id"))
            serializer = QuizSerializer(response,many=True)
            return Response(serializer.data)
        
        elif self.request.GET.get("quiz_id") and id is not None:
            answer = Answer.objects.filter(student=id,question__quiz=self.request.GET.get("quiz_id"))
            serializer = AnswerSerializer(answer,many=True)
            return Response(serializer.data)

        answer = Answer.objects.filter(student=id)
        serializer = AnswerSerializer(answer,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer=AnswerSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,id):
        answer=self.get_object(id)
        serializer=AnswerSerializer(answer,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ActivityViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class=ActivitySerializer               
    queryset=Activity.objects.all()    

    

