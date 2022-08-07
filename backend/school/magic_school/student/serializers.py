from asyncio.windows_events import NULL
from asyncore import write
from cProfile import Profile
from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from django.db.models import Avg, Max, Min, Sum

from .models import Classroom ,Profile,Attendance,Answer


from .models import HomeworkTeacher, Student,Subject,Mark,HomeWorkStudent,DailyLessons,Activity
from django.contrib.auth import get_user_model

User = get_user_model()

class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    classroom=serializers.SlugRelatedField(many=False, slug_field="name",queryset=Classroom.objects.all())
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
            "phone",
            "photo",
            "address",
            'classroom',
            'username',
            'password',
            )
        
    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        user = User(username=username, account_type=User.Student)
        user.set_password(password)
        user.save()
        validated_data['user'] = user
        obj = super(StudentSerializer, self).create(validated_data)
        return obj
    
    
class StudentSerializerGET(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    password = serializers.SerializerMethodField()
    classroom=serializers.SlugRelatedField(many=False, slug_field="name",queryset=Classroom.objects.all())
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
            "phone",
            "photo",
            'classroom',
            'username',
            'password',
            )
    def get_username(self,obj):
        obj=Student.objects.get(id=self.context["student"]).user.username
        return obj
    def get_password(self,obj):
        obj=Student.objects.get(id=self.context["student"]).user.password
        return obj

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
    subject=serializers.CharField(max_length =40)
    average=serializers.IntegerField()
        

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
    def create(self, validated_data):
        obj = HomeworkTeacher.objects.create(**validated_data)
        classroom=validated_data.get("classroom").id
        queryset=Student.objects.filter(classroom=classroom)
        for i in range (len(queryset)):
            HomeWorkStudent.objects.create(homework=obj,student=queryset[i],status=False,pdf_from_student=NULL)
        return  obj       



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


class DailyLessonsListSerializer(serializers.ListSerializer):
     def update(self, instance, validated_data):
        ret = []
        for data in validated_data:
            if data.get('id') not in {'', None}:
                DailyLessons.objects.filter(id=data['id']).update(**data)
                ret.append(data)
            else:
                ret.append(DailyLessons.objects.create(**data))
        return ret 



class DailyLessonsSerializer(serializers.ModelSerializer):
    className=serializers.SlugRelatedField(many=False, slug_field="name",queryset=Classroom.objects.all())
    teacher=serializers.SlugRelatedField(many=False, slug_field="first_name",queryset=Profile.objects.filter(user__account_type="Teacher"))
    subject=serializers.SlugRelatedField(many=False, slug_field="subject_name",queryset=Subject.objects.all())
    class Meta:
        model=DailyLessons
        list_serializer_class = DailyLessonsListSerializer
        fields=(
            "id",
            "className",
            "day",
            "period",
            "teacher",
            "subject",
        )    



class CountSerializer(serializers.Serializer):
    attendance_status = serializers.CharField(max_length =10)
    count = serializers.IntegerField()

class MonthlyAttendance(serializers.Serializer):
    attendance_status = serializers.CharField(max_length =10)
    count = serializers.IntegerField()
    month = serializers.DateField()

class AnswerListSerializer(serializers.ListSerializer):
     def update(self, instance, validated_data):
        ret = []
        for data in validated_data:
            if data.get('id') not in {'', None}:
                Answer.objects.filter(id=data['id']).update(**data)
                ret.append(data)
            else:
                ret.append(Answer.objects.create(**data))
        return ret 

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = AnswerListSerializer
        model=Answer
        fields="__all__"

class AttendanceSerializer(serializers.ModelSerializer): 

    class Meta:
        model = Attendance
        fields = "__all__"



class ActivitySerializer(serializers.ModelSerializer):
    student=serializers.SlugRelatedField(many=False, slug_field="first_name",queryset=Student.objects.all())
    subject=serializers.SlugRelatedField(many=False, slug_field="subject_name",queryset=Subject.objects.all())
    class Meta:
        model=Activity
        fields=(
            "student",
            "subject",
            "description",
            "star",
            "date",
            "condition",
        )        