from cProfile import Profile
from telnetlib import STATUS
from django.db.models import Count
from django.db.models.functions import TruncMonth 
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from .models import  HomeWorkStudent,Profile,face_recognition,Attendance
from .models import Student,Subject,Mark,HomeworkTeacher,DailyLessons


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
                            
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.http import JsonResponse

def StudentAttendance(request,student_id):
    if  student_id:
        query = (Attendance.objects.filter(student=Student.objects.get(id=student_id))
        .values("attendance_status")
        .annotate(count=Count("attendance_status"))
        .order_by())
        response = AttendanceSerializer(query,many=True)
        return JsonResponse(response.data,safe=False)

def StudentAttendanceMonthly(request,student_id):
    query = (Attendance.objects.filter(student=Student.objects.get(id=student_id))
            .annotate(month=TruncMonth("day"))
            .values("month")
            .annotate(count=Count("attendance_status"))
            .values("month","count","attendance_status")
            .order_by("month"))

    response = MonthlyAttendance(query,many=True)
    return JsonResponse(response.data,safe=False)




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
    def get_queryset(self):
        queryset=super(DailyLessonsViewSit,self).get_queryset()
        if self.request.GET.get("className"):
            return queryset.filter(className=self.request.GET.get("className"))
        elif self.request.GET.get("teacher"):
            return queryset.filter(teacher=self.request.GET.get("teacher"))
        return queryset 

class RecognizeFace(APIView):
    def post(self,request):
        im = request.data.get('face')
        # image = np.array(im)
        recognizer = face_recognition()
        queryset = Student.objects.all()
        id = recognizer.recognize_face(im,queryset)
        if id == "not recognized":
            return Response(id)
        student_attendance =Attendance(
            student=Student.objects.get(id=id),
            attendance_status="present")
        student_attendance.save()
        return Response(id)
    
    