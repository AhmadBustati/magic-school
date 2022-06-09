from rest_framework import serializers
from .models import Classroom, Feedback, Holiday, Post, Profile

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
            "title",
            "birthday",
            "gender",
            "age",
            "phone",
            "photo",
            'classroom',
            'username',
            'password',
            "account_type",

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


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = (
            "id",
            "type",
            "text",
            "user",
        )



