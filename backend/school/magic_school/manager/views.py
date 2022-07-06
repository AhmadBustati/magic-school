from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import Classroom, Feedback, Holiday, Post, Profile,Message,QuizName,Question
from .serializers import ClassroomSerializer, HolidaySerializer, PostSerializer, ProfileSerializer, FeedbackSerializer,MessageSerializer
from .apps import ManagerConfig

from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.contrib.auth import get_user_model

from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response

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



class QuestionGenerator(APIView):
    def post(self, request):
        model = ManagerConfig.model
        tokenizer = ManagerConfig.tokenizer
        text = request.data.get('text')
        profile = Profile.objects.get(id=request.data.get('profile_id'))
        class_name = Classroom.objects.get(id=request.data.get('class_name_id'))
        a = QuizName(
            name=request.data.get('name'),
            profile=profile,
            class_name=class_name,
        
        )


        a.save()

        question_list = []
        key="question"
        for t in text :
            input_ids, attention_mask = self.encode_text(t, tokenizer)
            outputs = model.generate(input_ids,attention_mask=attention_mask)
            question= tokenizer.decode(outputs[0],skip_special_tokens=True)
            Question(question_text=question, quiz=a).save()
            question_list.append(question)

        response_dict = {}
        response_dict.setdefault(key,question_list)
       
        return Response(response_dict)

    def encode_text(self,text, tokenizer):
        encoded_text = tokenizer(
        text,
        padding = "max_length",
        max_length = 512,
        truncation = True,
        return_tensors = "tf"
    )
        input_ids = encoded_text["input_ids"]
        attention_mask = encoded_text["attention_mask"]
        return input_ids, attention_mask



