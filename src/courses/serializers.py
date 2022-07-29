from rest_framework import serializers
from . import models
from src.profiles.models import FatUser
from .validators import StudentWorkValidator


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
        model = models.Tags
        fields = ('name',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
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
        ref_name = 'userCourse'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lesson
        fields = (
            'lesson_type',
            'name',
            'viewed',
            'video_url',
            'published',
            'slug',
            'description',
            'hint'
        )


class DetailLessonSerializer(serializers.ModelSerializer):
    code = CodeQuestionSerializer(many=True)
    quiz = QuizSerializer(many=True)
    work = serializers.SerializerMethodField()

    class Meta:
        model = models.Lesson
        fields = (
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


class ListCourseSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    tags = TagSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = models.Course
        fields = (
            'author',
            'tags',
            'category',
            'name',
            'description',
            'published',
            'updated',
            'slug',
            'id',
            'view_count'
        )


class DetailCourseSerializer(serializers.ModelSerializer):
    mentor = UserSerializer()
    author = UserSerializer()
    tags = TagSerializer(many=True)
    category = CategorySerializer()
    lessons = LessonSerializer(many=True)

    class Meta:
        model = models.Course
        fields = (
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


class StudentWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentWork
        fields = ('lesson', 'code_answer', 'quiz_answer', 'completed', )

    def validate(self, data):
        validate_class = StudentWorkValidator()
        validate_class(data)
        return data

    def create(self, validated_data):
        return models.StudentWork.objects.create(**validated_data, student=self.context['request'].user)


class HelpUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HelpUser
        fields = ('lesson',)

    def create(self, validated_data):
        mentor = validated_data['lesson'].course.mentor
        student = self.context['request'].user
        return models.HelpUser.objects.create(mentor=mentor, student=student, **validated_data)


