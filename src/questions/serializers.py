from rest_framework import serializers
from . import models
from src.courses.serializers import UserSerializer


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tags
        fields = ('name',)


class AnswerSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = models.Answer
        fields = (
            'author',
            'text',
            'parent',
            'date',
            'updated',
            'rating',
            'accepted'
        )


class RetrieveQuestionSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    answer = AnswerSerializer(many=True)

    class Meta:
        model = models.Question
        fields = (
            'asked',
            'viewed',
            'text',
            'tags',
            'rating',
            'author',
            'updated',
            'answer',
            'title'
        )


class ListQuestionSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    correct_answers = serializers.SerializerMethodField()
    answer_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Question
        fields = ('title', 'rating', 'author', 'viewed', 'correct_answers')

    def get_correct_answers(self, instance):
        return instance.correct_answers_count()

    def get_answer_count(self, instance):
        return instance.answers_count()


class QuestionReview(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionReview
        fields = ('grade', 'question')


class AnswerReview(serializers.ModelSerializer):
    class Meta:
        model = models.AnswerReview
        fields = ('grade', 'answer')
