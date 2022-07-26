from rest_framework import serializers
from . import models
from src.courses.serializers import UserSerializer
from rest_framework import status


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tags
        fields = ('name',)


class AnswerSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False)
    children = serializers.SerializerMethodField()

    class Meta:
        model = models.Answer
        fields = (
            'author',
            'text',
            'parent',
            'date',
            'updated',
            'rating',
            'accepted',
            'question',
            'children'
        )

    def create(self, validated_data):
        user = self.context['request'].user
        answer = models.Answer.objects.create(
            question=validated_data['question'],
            author=user
        )
        return answer

    def get_children(self, instance):
        children = models.Answer.objects.filter(parent=instance)
        serializer = AnswerSerializer(children, many=True)
        return serializer.data


class RetrieveQuestionSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)

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
            'answers',
            'title'
        )


class ListQuestionSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    correct_answers = serializers.SerializerMethodField()
    answer_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Question
        fields = (
            'title',
            'rating',
            'author',
            'viewed',
            'correct_answers',
            'answer_count'
        )

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


class UpdateQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ('text',)

    def validate(self, data):
        if self.context['request'].user is not self.instance.author:
            serializers.ValidationError({
                'error': 'Вы не можете изменить чужой вопрос'
            },
                status.HTTP_403_FORBIDDEN
            )
        return data


class UpdateAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ('text',)