from rest_framework import serializers

import json
import requests.exceptions

from src.profiles.models import FatUser
from .validators import StudentWorkValidator
from .service import Service
from .models import Course, CodeQuestion, Quiz, Tag, Category, Lesson, StudentWork, HelpUser


class CodeQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeQuestion
        fields = ('code', 'answer')
        read_only_fields = ('code', 'answer')


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ('text', 'lesson')
        read_only_fields = ('right', 'hint')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'parent')
        ref_name = 'courses_category'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FatUser
        fields = (
            'socials',
            'first_name',
            'last_name',
            'avatar',
        )
        ref_name = "Fat user"


class LessonSerializer(serializers.ModelSerializer):
    """Lesson"""
    code = CodeQuestionSerializer(many=True)
    quiz = QuizSerializer(many=True)
    work = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = [
            'id', 'lesson_type', 'name', 'viewed', 'video_url', 'published',
            'slug', 'description', 'hint', 'code', 'quiz', 'work'
        ]

    def get_work(self, instance):
        user = self.context['request'].user
        work = StudentWork.objects.filter(student=user.id, lesson=instance).first()
        serialize_work = StudentWorkSerializer(work)
        return serialize_work.data


class CourseSerializer(serializers.ModelSerializer):
    """Course"""
    author = UserSerializer()
    tags = TagSerializer(many=True)
    lessons = LessonSerializer(many=True)
    category = CategorySerializer()
    mentor = UserSerializer()

    class Meta:
        model = Course
        fields = [
            'name', 'description', 'slug', 'view_count', 'published',
            'updated', 'author', 'students', 'category', 'mentor', 'tags', 'lessons'
        ]


class StudentWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentWork
        fields = ('lesson', 'code_answer', 'quiz_answer', 'completed', 'error')

    def validate(self, data):
        validate_class = StudentWorkValidator()
        validate_class(data)
        return data

    def create(self, validated_data):
        work = StudentWork.objects.create(**validated_data, student=self.context['request'].user)
        file = work.create_testfile()
        service = Service()
        try:
            service.request(file, validated_data['lesson'].course.name)
            if service.status_code == 200:
                body = json.loads(service.content)
                if 'test_django exited with code 0' in body['result']['stdout']:
                    work.completed = True
                    return work
                work.error = body['result']['stdout']
        except requests.exceptions.ConnectionError:
            raise serializers.ValidationError('server not allowed')
        return work


class HelpUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpUser
        fields = ('lesson',)

    def create(self, validated_data):
        mentor = validated_data['lesson'].course.mentor
        student = self.context['request'].user
        return HelpUser.objects.create(mentor=mentor, student=student, **validated_data)
