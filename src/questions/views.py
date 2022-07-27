from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from . import serializers
from rest_framework.permissions import IsAuthenticated
from .models import Question, Answer, QuestionReview, AnswerReview


class ListQuestionsView(ListAPIView):
    serializer_class = serializers.ListQuestionSerializer
    queryset = Question.objects.all()


class RetrieveQuestionView(RetrieveAPIView):
    serializer_class = serializers.RetrieveQuestionSerializer
    queryset = Question.objects.all()
    lookup_field = 'id'


class CreateAnswerView(CreateAPIView):
    serializer_class = serializers.AnswerSerializer
    permission_classes = [IsAuthenticated]
    queryset = Answer.objects.all()


class UpdateQuestionView(UpdateAPIView):
    serializer_class = serializers.UpdateQuestionSerializer
    permission_classes = [IsAuthenticated]
    queryset = Question.objects.all()
    lookup_field = 'id'


class UpdateAnswerView(UpdateAPIView):
    serializer_class = serializers.UpdateAnswerSerializer
    permission_classes = [IsAuthenticated]
    queryset = Answer.objects.all()
    lookup_field = 'id'


class DestroyAnswerView(DestroyAPIView):
    serializer_class = serializers.AnswerSerializer
    permission_classes = [IsAuthenticated]
    queryset = Answer.objects.all()
    lookup_field = 'id'


class DestroyQuestionView(DestroyAPIView):
    serializer_class = serializers.RetrieveQuestionSerializer
    permission_classes = [IsAuthenticated]
    queryset = Question.objects.all()
    lookup_field = 'id'


class CreateQuestionReview(CreateAPIView):
    serializer_class = serializers.QuestionReviewSerializer
    permission_classes = [IsAuthenticated]
    queryset = QuestionReview.objects.all()


class CreateAnswerReview(CreateAPIView):
    serializer_class = serializers.AnswerReviewSerializer
    permission_classes = [IsAuthenticated]
    queryset = AnswerReview.objects.all()