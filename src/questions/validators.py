from rest_framework import serializers
from . import models


class QuestionValidator:

    def check_review(self, data):
        if 'question' in data:
            if models.QuestionReview.objects.filter(**data).exists():
                raise serializers.ValidationError({'error': 'Пользователь уже оставил отзыв'})
        else:
            if models.AnswerReview.objects.filter(**data).exists():
                raise serializers.ValidationError({'error': 'Пользователь уже оставил отзыв'})