from rest_framework import serializers
from .models import *
from src.profiles.models import FatUser
from .validators import StudentWorkValidator


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
            'socials',
            'first_name',
            'last_name',
            'avatar',
        )


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
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
        model = Lesson
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
        work = StudentWork.objects.filter(student=user, lesson=instance).first()
        serialize_work = StudentWorkSerializer(work)
        return serialize_work.data


class ListCourseSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    tags = TagSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Course
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
        model = Course
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
        model = StudentWork
        fields = ('lesson', 'code_answer', 'quiz_answer', 'completed', )

    def validate(self, data):
        validate_class = StudentWorkValidator()
        validate_class(data)
        return data

    def create(self, validated_data):
        return StudentWork.objects.create(**validated_data, student=self.context['request'].user)


class HelpUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpUser
        fields = ('lesson',)

    def create(self, validated_data):
        mentor = validated_data['lesson'].course.mentor
        student = self.context['request'].user
        return HelpUser.objects.create(mentor=mentor, student=student, **validated_data)