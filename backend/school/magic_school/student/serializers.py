from asyncore import write
from dataclasses import fields
from pyexpat import model
from rest_framework import serializers

#from school.magic_school.manager.models import Classroom , Profile
from .models import Student,Subject,Mark
from django.contrib.auth import get_user_model

User = get_user_model()

class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Student
        fields = (
            "id",
            "first_name", 
            "last_name",
            "father_name",
            "mother_name",
            "birthday",
            "gender",
            "age",
            "phone",
            "photo",
            'classroom',
            'username',
            'password',
            )

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        user = User.objects.create(username=username, password=password, account_type=User.Student)
        validated_data['user'] = user
        obj = super(StudentSerializer, self).create(validated_data)
        return obj


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subject
        fields="__all__"

class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model=Mark
        fields=(
            "id",
            "term_name",
            "classroom",
            "subject",
            "student",
            "exam_name",
            "mark",
            "fullmark",
        )
    
