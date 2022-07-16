from rest_framework import serializers
from .models import *
from src.profiles.models import FatUser


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('name',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'parent')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FatUser
        fields = (
            'socials', 'first_name',
            'last_name', 'avatar',
        )


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            'lesson_type', 'name',
            'viewed', 'video_url',
            'published', 'slug',
            'description',
        )


class ListCourseSerializer(serializers.ModelSerializer):
    autor = UserSerializer()
    tags = TagSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Course
        fields = (
            'autor', 'tags',
            'category', 'name',
            'description', 'published',
            'updated', 'slug',
            'id', 'view_count'
        )


class DetailCourseSerializer(serializers.ModelSerializer):
    mentor = UserSerializer()
    autor = UserSerializer()
    tags = TagSerializer(many=True)
    category = CategorySerializer()
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Course
        fields = (
            'name', 'description',
            'slug', 'view_count',
            'published', 'updated',
            'mentor', 'autor',
            'tags', 'category',
            'lessons',
        )


