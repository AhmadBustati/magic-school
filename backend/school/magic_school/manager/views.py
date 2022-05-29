from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import Classroom, Feedback, Holiday, Post, Profile
from .serializers import ClassroomSerializer, HolidaySerializer, PostSerializer, ProfileSerializer, FeedbackSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


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


