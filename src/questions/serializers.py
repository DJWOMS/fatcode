from rest_framework import serializers
from . import models
from .validators import QuestionValidator
from ..profiles.serializers import GetUserSerializer


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ("id", "name")
        read_only_fields = ("id",)


class AnswerSerializer(serializers.ModelSerializer):
    author = GetUserSerializer(required=False)
    children = serializers.SerializerMethodField()

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
            "children",
        )

    def create(self, validated_data):
        return models.Answer.objects.create(question=validated_data["question"])

    def get_children(self, instance):
        children = models.Answer.objects.filter(parent=instance)
        serializer = AnswerSerializer(children, many=True).data
        return serializer.data


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
        return instance.correct_answers_count()

    def get_answer_count(self, instance):
        return instance.answers_count()


class QuestionReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionReview
        fields = ("grade", "question")

    def validate(self, data):
        data["user"] = self.context["request"].user
        QuestionValidator().check_review(data)
        return data

    def create(self, validated_data):
        review = self.Meta.model.objects.create(**validated_data)
        validated_data["question"].update_rating()
        return review


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
        instance = super(UpdateQuestionSerializer, self).update(instance, validated_data)

        for tag_data in tags_data:
            tag_qs = models.Tag.objects.filter(name__iexact=tag_data["name"])
            if tag_qs.exists():
                tag = tag_qs.first()
            else:
                tag = models.Tag.objects.create(**tag_data)
            instance.tags.add(tag)
        return instance


class UpdateAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ("text",)
