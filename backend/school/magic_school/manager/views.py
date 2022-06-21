from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import Classroom, Feedback, Holiday, Post, Profile,Message
from .serializers import ClassroomSerializer, HolidaySerializer, PostSerializer, ProfileSerializer, FeedbackSerializer,MessageSerializer

from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.contrib.auth import get_user_model

from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

User = get_user_model()

def AdminNumber(request):
    dd=str(User.objects.filter(account_type="employee").count())
    response={
        "number":dd
    }
    return JsonResponse(response)

def StudentNumber(request):
    dd=str(User.objects.filter(account_type="student").count())
    response={
        "number":dd
    }
    return JsonResponse(response)

def TeacherNumber(request):
    dd=str(User.objects.filter(account_type="teacher").count())
    response={
        "number":dd
    }
    return JsonResponse(response)    


class PostViewSet(ModelViewSet, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)


class HolidayViewSet(ModelViewSet, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    def perform_create(self, serializer):
        user=self.request.user  
        instance = serializer.save(head_teacher=User.objects.get(id=user.id))    


class ClassroomViewSet(ModelViewSet, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer


class ProfileViewSet(ModelViewSet, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.filter(
        Q(user__account_type=User.Employee) | Q(user__account_type=User.Teacher))
    serializer_class = ProfileSerializer

    def get_queryset(self):  # for get all teachers or employees
        queryset = super(ProfileViewSet, self).get_queryset()
        
        if self.request.GET.get('type'):
            return queryset.filter(user__account_type=self.request.GET.get('type'))
        return queryset


class FeedbackViewSet(ModelViewSet, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class MessageViewSet(ModelViewSet, GenericViewSet):
    ermission_classes = [IsAuthenticated]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    ################ sender with authentication ###########################
    def perform_create(self, serializer):
        user=self.request.user  
        instance = serializer.save(sender=User.objects.get(id=user.id))

    ################ get message by user authentication ###########################    
    def get_queryset(self):
        queryset=super(MessageViewSet,self).get_queryset()
        if self.request.GET.get("person"):
            user=self.request.user
            userMessage=Message.objects.filter(
                Q(sender=User.objects.get(id=user.id))|Q(receiver=User.objects.get(id=user.id))
                )

            return userMessage.filter(
                Q(sender=self.request.GET.get("person"))|Q(receiver=self.request.GET.get("person")))
        else:    
            user=self.request.user  
            return Message.objects.filter(
                Q(sender=User.objects.get(id=user.id))|Q(receiver=User.objects.get(id=user.id))
                )




