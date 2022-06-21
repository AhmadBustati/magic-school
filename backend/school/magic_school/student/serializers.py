from asyncore import write
from cProfile import Profile
from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from django.db.models import Avg, Max, Min, Sum
from .models import Classroom ,Profile


from .models import HomeworkTeacher, Student,Subject,Mark,HomeWorkStudent,DailyLessons
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
            "user",
            'username',
            'password',
            )
        depth=1
    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        user = User(username=username, account_type=User.Student)
        user.set_password(password)
        user.save()
        validated_data['user'] = user
        obj = super(StudentSerializer, self).create(validated_data)
        return obj
    
    
    # def get_username(self,obj):
    #     obj=Student.objects.get(id=self.context["student"]).user.username
    #     return obj
    # def get_password(self,obj):
    #     obj=Student.objects.get(id=self.context["student"]).user.password
    #     return obj


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subject
        fields="__all__"

class MarkSerializer(serializers.ModelSerializer):
    classroom=serializers.SlugRelatedField(many=False, slug_field="name",queryset=Classroom.objects.all())
    subject=serializers.SlugRelatedField(many=False, slug_field="subject_name",queryset=Subject.objects.all())
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

class AverageSerializer(serializers.ModelSerializer):
    average=serializers.SerializerMethodField()
    subject=serializers.SerializerMethodField()
    class Meta:
        model=Mark
        fields=(
            "subject",
            "average",
        )

    def get_average(self,obj):
        avg=Mark.objects.filter(
            student=self.context["student"],
            subject=self.context["subject"]).aggregate(avge=(Sum("mark")/Sum("fullmark"))*100).get("avge",0.00)  
        return avg
    def get_subject(self,obj):
        obj=Subject.objects.get(id=self.context["subject"])
        return obj.subject_name

        

class HomeWorkeTeacherSerializer(serializers.ModelSerializer):
    classroom=serializers.SlugRelatedField(many=False, slug_field="name",queryset=Classroom.objects.all())
    subject=serializers.SlugRelatedField(many=False, slug_field="subject_name",queryset=Subject.objects.all())
    class Meta:
        model=HomeworkTeacher
        fields=(
            "id",
            "classroom",
            "subject",
            "description",
            "date",
            "pdf_from_teacher",
        )

class HomeWorkeStudentSerializer(serializers.ModelSerializer):
# post وما بدي ادخلو بال get هون بدي رقم الطالب بس ينعرض بال 
    class Meta:
        model=HomeWorkStudent
        fields=(
            "id",
            "homework",
            "student",
            "status",
            "pdf_from_student",
        )

class DailyLessonsSerializer(serializers.ModelSerializer):
    className=serializers.SlugRelatedField(many=False, slug_field="name",queryset=Classroom.objects.all())
    subject=serializers.SlugRelatedField(many=False, slug_field="subject_name",queryset=Subject.objects.all())
    teacher=serializers.SlugRelatedField(many=False, slug_field="id",queryset=Profile.objects.filter(user__account_type="Teacher"))
    class Meta:
        model=DailyLessons
        fields=(
            "id",
            "className",
            "day",
            "period",
            "subject",
            "teacher",
        )        