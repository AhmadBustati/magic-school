from re import M
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models


class User(AbstractUser):
    Student="student"
    Teacher="teacher"
    Employee="employee"
    Manager = "manager"
    ACCOUNT_TYPES = (
        (Student,"Student"),
        (Teacher, "Teacher"),
        (Employee, "Employee"),
        (Manager, "Manager"),
    )


    name = CharField(_("Name of User"), blank=True, max_length=255)
    account_type = models.CharField(
        max_length=15, choices=ACCOUNT_TYPES, default= Manager
    )

    @property
    def is_student(self):
        return self.account_type == self.Student

    @property
    def is_teacher(self):
        return self.account_type == self.Teacher

    @property
    def is_Employee(self):
        return self.account_type == self.Employee

    @property
    def is_manager(self):
        return self.account_type == self.Manager
        
    def get_absolute_url(self):
        return reverse("user:detail", kwargs={"username": self.username})


class Message(models.Model):
     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')        
     receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')        
     message = models.CharField(max_length=1200)
     timestamp = models.DateTimeField(auto_now_add=True)
     is_read = models.BooleanField(default=False)
     def __str__(self):
           return self.message
     class Meta:
           ordering = ('timestamp',) 