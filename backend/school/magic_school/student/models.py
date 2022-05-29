from django.db import models

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
    Month = 'monday'
    Tus = 'tuesday'
    Wed = 'wensday'
    Thu = 'thursday'
    First = 'first'
    DAYS = (
        ('1', 'sunday'),
        ('2', 'monday'),
        ('3', 'tuesday'),
        ('4', 'wensday'),
        ('5', 'thursday'),
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
    day = models.CharField(choices=DAYS, max_length=30)
    period = models.CharField(choices=PERIOD, max_length=30)
