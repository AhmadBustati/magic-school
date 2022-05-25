from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import Classroom
from .models import Student,Subject,Mark
from django.http import Http404

from .serializers import StudentSerializer,SubjectSerializer,MarkSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


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
        return Response(serializer.datak)

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
            return queryset.filter(student=self.request.GET.get('student'),subject=self.request.GET.get('subject'))
            
        return  queryset  
               
                          

