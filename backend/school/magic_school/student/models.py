from django.db import models
from manager.models import Profile

from manager.models import Classroom
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model

User = get_user_model()


class Student(models.Model):
    
    F = "female"
    M = "male"

    GENDER_TYPES = (
        (M, 'male'),
        (F, 'female'),
    )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    father_name = models.CharField(max_length=20, null=True, blank=True)
    mother_name = models.CharField(max_length=20, null=True, blank=True)
    age = models.IntegerField()
    birthday = models.DateField()
    gender = models.CharField(choices=GENDER_TYPES, max_length=20, default=M)
    phone = PhoneNumberField(null=True, blank=True, unique=True)
    photo = models.ImageField(upload_to='photo', null=True, blank=True)
    user = models.ForeignKey(
        User,
        related_name="user_student",
        on_delete=models.CASCADE,
        limit_choices_to={"account_type": User.Student},

    )
    classroom = models.ForeignKey(
        Classroom, related_name='student_classroom', on_delete=models.CASCADE)
    def __str__(self):
        return self.first_name

class Subject(models.Model):
    subject_name = models.CharField(max_length=20)

    def __str__(self):
        return self.subject_name


class Mark(models.Model):
    term1="Term1"
    term2="Term2"
    TERM_NAME=(
        (term1, '1'),
        (term2, '2'),
    )

    term_name=models.CharField(choices=TERM_NAME,max_length=20)
    classroom=models.ForeignKey(
        Classroom, related_name="classroom_mark",on_delete=models.CASCADE,
    )
    subject = models.ForeignKey(
        Subject, related_name="subject_mark", on_delete=models.CASCADE)
    student = models.ForeignKey(
        Student, related_name="student_mark", on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=100)
    mark = models.IntegerField()
    fullmark = models.IntegerField()


class DailyLessons(models.Model):
    Sun = 'sunday'
    Mon = 'monday'
    Tus = 'tuesday'
    Wed = 'wensday'
    Ther = 'thursday'
    DAYS = (
        (Sun, '1'),
        (Mon, '2'),
        (Tus, '3'),
        (Wed, '4'),
        (Ther, '5'),
    )
    one = 'first'
    two = 'second'
    three = 'third'
    four = 'fourth'
    five = 'fifth'
    six = 'sixth'
    seven = 'seventh'
    PERIOD = (
        (one, '1'),
        (two, '2'),
        (three, '3'),
        (four, '4'),
        (five, '5'),
        (six, '6'),
        (seven, '7'),
    )
    className = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher=models.ForeignKey(
        Profile,
        related_name="teacher_daelylessons",
        on_delete=models.CASCADE,
        limit_choices_to={"user__account_type":User.Teacher},
    )
    day = models.CharField(choices=DAYS, max_length=30)
    period = models.CharField(choices=PERIOD, max_length=30)



class HomeworkTeacher(models.Model):
    classroom=models.ForeignKey(
        Classroom,
        related_name="classroom_homeworkteacher",
        on_delete=models.CASCADE,
    )
    subject=models.ForeignKey(
        Subject,
        related_name="subject_homeworkteacher",
        on_delete=models.CASCADE,
    )
    teacher=models.ForeignKey(
        Profile,
        related_name="teacher_homeworkteacher",
        on_delete=models.CASCADE,
        limit_choices_to={"user__account_type":User.Teacher},
    )
    description=models.TextField()
    date=models.DateField(auto_now=True)
    pdf_from_teacher=models.FileField(upload_to="pdf_teacher/",null=True,blank=True,) 

class HomeWorkStudent(models.Model):
    homework=models.ForeignKey(HomeworkTeacher,related_name="homework_homework",on_delete=models.CASCADE) 
    student=models.ForeignKey(
                                Student,
                                related_name="student_homework",
                                on_delete=models.CASCADE,
                                limit_choices_to={"user__account_type":User.Student},
                                )
    status=models.BooleanField()
    pdf_from_student=models.FileField(upload_to="pdf_student/",null=True,blank=True)
    