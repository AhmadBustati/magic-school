from django.db import models
from django.db.models import Q

from django_extensions.db.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model

User = get_user_model()


class Classroom(models.Model):
    name = models.CharField(max_length=20)


class Profile(models.Model):
    F = "female"
    M = "male"

    GENDER_TYPES = (
        (M, 'male'),
        (F, 'female'),
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    father_name = models.CharField(max_length=30, null=True, blank=True)
    certificates = models.CharField(max_length=100)
    age = models.IntegerField()
    birthday = models.DateField()
    gender = models.CharField(choices=GENDER_TYPES, max_length=20, default=M)
    phone = PhoneNumberField(null=True, blank=True, unique=True)
    title = models.CharField(max_length=30, null=True, blank=True)
    classroom = models.ForeignKey(
        Classroom, related_name='teacher_classroom', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photo', null=True, blank=True)
    user = models.ForeignKey(
        User,
        related_name="user_profile",
        on_delete=models.CASCADE,
        limit_choices_to=Q(account_type=User.Employee) | Q(
            account_type=User.Teacher),
    )

    def str(self):
        return self.first_name


class Post(TimeStampedModel):
    date=models.DateField(auto_now=True)  
    timee=models.TimeField(auto_now=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='media', null=True, blank=True)
    user = models.ForeignKey(
        User,
        related_name="user_admin_post",
        on_delete=models.CASCADE,
        limit_choices_to={"account_type": User.Manager},
    )

    def __str__(self):
        return f"{self.user}: {self.description}"


class Holiday(TimeStampedModel):
    day = models.DateField()
    description = models.TextField(null=True, blank=True)
    name_of_holiday = models.CharField(max_length=255)

    def __str__(self):
        return self.name_of_holiday

# update
class Feedback(models.Model):
    Suggestion = "suggestion"
    Complaint = "complaint"
    TYPE = (
        (Suggestion, 'suggestion'),
        (Complaint, 'complaints'),
    )
    user = models.ForeignKey(
        User,
        related_name="manager_feedbacks",
        on_delete=models.CASCADE,
        limit_choices_to={"account_type": User.Manager},
    )
    type = models.CharField(choices=TYPE, max_length=20)
    text = models.TextField()
