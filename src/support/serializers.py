from rest_framework import serializers
from ..profiles.serializers import GetUserSerializer

from . import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('id', 'name')
        ref_name = 'support_category'


class SupportAnswerSerializer(serializers.ModelSerializer):
    """Ответ пользователю"""

    class Meta:
        model = models.Answer
        fields = ("id", "report", "text")


class ReportListSerializer(serializers.ModelSerializer):
    """Список ошибок от пользователя"""

    class Meta:
        model = models.Report
        fields = ("id", "category", "text", "status")


class ReportCreateSerializer(serializers.ModelSerializer):
    """Создание ошибки пользователем"""

    class Meta:
        model = models.Report
        fields = ("category", "text", "image", "video")


class ReportDetailSerializer(serializers.ModelSerializer):
    """Ошибка пользователя детально с ответом"""
    user = GetUserSerializer()
    answers = SupportAnswerSerializer(many=True)

    class Meta:
        model = models.Report
        fields = (
            "id",
            "category",
            "user",
            "text",
            "status",
            "answers",
            "image",
            "video",
        )
