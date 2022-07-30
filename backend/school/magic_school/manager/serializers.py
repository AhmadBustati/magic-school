from rest_framework import serializers

from student.models import Answer, Student
from .models import Classroom, Feedback, Holiday, Post, Profile,Message,Question,QuizName

from django.contrib.auth import get_user_model

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "description", "image","date","timee")


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = ("id", 'day', 'description', 'name_of_holiday')


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ("id", 'name')


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    account_type = serializers.CharField(write_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "first_name",
            "last_name",
            "father_name",
            "certificates",
            "job_title",
            "birthday",
            "gender",
            "phone",
            "photo",
            'username',
            'password',
            "account_type",
            "address",
        )
        
    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        account_type = validated_data.pop('account_type')
        user = User(
            username=username,account_type=account_type)
        user.set_password(password) 
        user.save()       
        validated_data['user'] = user
        obj = super(ProfileSerializer, self).create(validated_data)
        return obj

class SerrializerManagerGET(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    password = serializers.SerializerMethodField()
    account_type=serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = (
            "id",
            "first_name",
            "last_name",
            "father_name",
            "certificates",
            "job_title",
            "birthday",
            "gender",
            "phone",
            "photo",
            'username',
            'password',
            "account_type",
            "address",
        )
    def get_username(self,obj):
        obj=Profile.objects.get(id=self.context["profile"]).user.username
        return obj
    def get_password(self,obj):
        obj=Profile.objects.get(id=self.context["profile"]).user.password
        return obj
    def get_account_type(self,obj):
        obj=Profile.objects.get(id=self.context["profile"]).user.account_type
        return obj  
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = (
            "id",
            "type",
            "text",
            "user",
        )


class MessageSerializer(serializers.ModelSerializer):
    """For Serializing Message"""
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all(),required=False)
    receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    class Meta:
        model = Message
        fields = (
            "sender",
            'receiver',
            'message',
            'timestamp',
            )

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id','question_text')
    
    def create(self, validated_data):
        obj = QuestionSerializer.objects.create(**validated_data)
        classroom=obj.quiz.class_name
        queryset=Student.objects.filter(classroom=classroom)
        for i in range (len(queryset)):
            Answer.objects.create(student=queryset[i],question=obj)
        return  obj   


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizName
        fields =('id','name','class_name','profile')