from rest_framework import serializers
from .models import *
from django.conf import settings


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('name')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'parent')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = (
            'username', 'first_name',
            'last_name', 'email',
            'first_login', 'avatar',
            'socials'
        )


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            'lesson_type', 'name',
            'viewed', 'video_url',
            'published', 'slug',
            'description'
        )


class CourseSerializer(serializers.ModelSerializer):
    mentor = UserSerializer()
    students = UserSerializer(many=True)
    autor = UserSerializer()
    tags = TagSerializer(many=True)
    category = CategorySerializer()
    lesson_set = LessonSerializer(many=True)

    class Meta:
        model = Course
        fields = (
            'name', 'description',
            'slug', 'view_count',
            'published', 'updated',
            'mentor', 'autor',
            'tags', 'students',
            'category', 'lesson_set'
        )

