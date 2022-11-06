from rest_framework import serializers
from . import models
from .validators import QuestionValidator
from ..profiles.serializers import GetUserSerializer
from .services import QuestionService, AnswerService


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ("id", "name")
        read_only_fields = ("id",)


class CreateAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ("text", "parent", "question")


class AnswerSerializer(serializers.ModelSerializer):
    author = GetUserSerializer(required=False)
    children_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Answer
        fields = (
            "author",
            "text",
            "parent",
            "date",
            "updated",
            "rating",
            "accepted",
            "question",
            "children_count",
        )

    def get_children_count(self, instance):
        children = instance.children.count()
        return children


class CreateQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ("title", "text")


class RetrieveQuestionSerializer(serializers.ModelSerializer):
    author = GetUserSerializer(read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)
    tags = TagsSerializer(many=True, read_only=True)

    class Meta:
        model = models.Question
        fields = (
            "asked",
            "viewed",
            "text",
            "tags",
            "rating",
            "author",
            "updated",
            "answers",
            "title",
        )


class ListQuestionSerializer(serializers.ModelSerializer):
    author = GetUserSerializer()
    correct_answers = serializers.SerializerMethodField()
    answer_count = serializers.SerializerMethodField()
    tags = TagsSerializer(many=True, read_only=True)

    class Meta:
        model = models.Question
        fields = (
            "title",
            "rating",
            "author",
            "viewed",
            "correct_answers",
            "answer_count",
            "tags",
        )

    def get_correct_answers(self, instance):
        service = QuestionService(instance)
        return service.correct_answers_count()

    def get_answer_count(self, instance):
        service = QuestionService(instance)
        return service.answers_count()


class QuestionReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionReview
        fields = ("grade", "question")

    def validate(self, data):
        data["user"] = self.context["request"].user
        QuestionValidator().check_review(data)
        return data


class AnswerReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnswerReview
        fields = ("grade", "answer")

    def validate(self, data):
        data["user"] = self.context["request"].user
        QuestionValidator().check_review(data)
        return data

    def create(self, validated_data):
        review = self.Meta.model.objects.create(**validated_data)
        validated_data["answer"].update_rating()
        return review


class UpdateQuestionSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True, read_only=False)

    class Meta:
        model = models.Question
        fields = ("title", "text", "tags")

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags")
        service = QuestionService(instance)
        service.update_tags(tags_data)
        instance = super(UpdateQuestionSerializer, self).update(instance, validated_data)
        return instance


class UpdateAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ("text",)


class UpdateAcceptAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ("accepted",)

    def update(self, instance, validated_data):
        AnswerService(instance).update_accept()
        instance = super(UpdateAcceptAnswerSerializer, self).update(instance, validated_data)
        return instance


class FollowerQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionFollowers
        fields = ('question',)


