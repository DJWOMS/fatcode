from rest_framework import serializers
from . import models


class QuestionValidator:

    def check_author(self, user, author):
        if user != author:
            raise serializers.ValidationError({
                'error': 'Вы не являетесь автором'
            })

    def check_review(self, data):
        if 'question' in data:
            if models.QuestionReview.objects.filter(
                    user=data['user'],
                    question=data['question'],
                    grade=data['grade']
            ).exists():
                raise serializers.ValidationError({'error': 'Пользователь уже оставил отзыв'})
        else:
            if models.AnswerReview.objects.filter(
                    user=data['user'],
                    answer=data['answer'],
                    grade=data['grade']
            ).exists():
                raise serializers.ValidationError({'error': 'Пользователь уже оставил отзыв'})