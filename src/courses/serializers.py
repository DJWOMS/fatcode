from rest_framework import serializers

from src.profiles.serializers import GetUserSerializer

from . import models
from .validators import StudentWorkValidator
from .services import Service


class CodeQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CodeQuestion
        fields = ('code', 'answer')
        read_only_fields = ('code', 'answer')


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Quiz
        fields = ('text', 'lesson')
        read_only_fields = ('right', 'hint')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ('name',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('name', 'parent')
        ref_name = 'courses_category'


class LessonDetailSerializer(serializers.ModelSerializer):
    """Урок"""
    code = CodeQuestionSerializer(many=True)
    quiz = QuizSerializer(many=True)
    work = serializers.SerializerMethodField()

    class Meta:
        model = models.Lesson
        fields = (
            'id',
            'lesson_type',
            'name',
            'viewed',
            'video_url',
            'published',
            'slug',
            'description',
            'code',
            'quiz',
            'work'
        )

    def get_work(self, instance):
        user = self.context['request'].user
        work = models.StudentWork.objects.filter(student=user, lesson=instance).first()
        serialize_work = StudentWorkSerializer(work)
        return serialize_work.data


class LessonListSerializer(serializers.ModelSerializer):
    """Список уроков"""

    class Meta:
        model = models.Lesson
        fields = (
            'id',
            'lesson_type',
            'name',
            'viewed',
            'video_url',
            'published',
            'slug',
            'description',
            'hint'
        )


class CourseSerializer(serializers.ModelSerializer):
    """Курс"""
    mentor = GetUserSerializer()
    author = GetUserSerializer()
    tags = TagSerializer(many=True)
    category = CategorySerializer()
    lessons = LessonListSerializer(many=True)

    class Meta:
        model = models.Course
        fields = (
            'id',
            'name',
            'description',
            'slug',
            'view_count',
            'published',
            'updated',
            'mentor',
            'author',
            'tags',
            'category',
            'lessons',
        )


class ListCourseSerializer(serializers.ModelSerializer):
    """Список курсов"""
    author = GetUserSerializer()
    tags = TagSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = models.Course
        fields = (
            'id',
            'author',
            'tags',
            'category',
            'name',
            'description',
            'published',
            'updated',
            'slug',
            'view_count'
        )


class StudentWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentWork
        fields = ('lesson', 'code_answer', 'quiz_answer', 'completed', 'error')

    def validate(self, data):
        validate_class = StudentWorkValidator()
        validate_class(data)
        return data

    def create(self, validated_data):
        work = models.StudentWork.objects.create(**validated_data, student=self.context['request'].user)
        file = work.create_testfile()
        service = Service()
        service.request(file, validated_data['lesson'].course.name)
        if service.status_code == 200:
            if 'test_django exited with code 0' in service.content['result']['stdout']:
                work.completed = True
                return work
            work.error = service.content['result']['stdout']
        return work


class HelpUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HelpUser
        fields = ('lesson',)

    def create(self, validated_data):
        mentor = validated_data['lesson'].course.mentor
        student = self.context['request'].user
        return models.HelpUser.objects.create(mentor=mentor, student=student, **validated_data)
