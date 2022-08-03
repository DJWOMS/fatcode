from . import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Question, Answer, QuestionReview, AnswerReview
from .permissions import IsAuthor


class ListQuestionsView(ModelViewSet):
    serializer_class = serializers.ListQuestionSerializer
    queryset = Question.objects.all()


class RetrieveQuestionView(ModelViewSet):
    serializer_class = serializers.RetrieveQuestionSerializer
    queryset = Question.objects.all()
    lookup_field = 'id'


class CreateAnswerView(ModelViewSet):
    serializer_class = serializers.AnswerSerializer
    permission_classes = [IsAuthenticated]
    queryset = Answer.objects.all()


class UpdateQuestionView(ModelViewSet):
    serializer_class = serializers.UpdateQuestionSerializer
    permission_classes = [IsAuthor]
    queryset = Question.objects.all()
    lookup_field = 'id'


class UpdateAnswerView(ModelViewSet):
    serializer_class = serializers.UpdateAnswerSerializer
    permission_classes = [IsAuthor]
    queryset = Answer.objects.all()
    lookup_field = 'id'


class DestroyAnswerView(ModelViewSet):
    serializer_class = serializers.AnswerSerializer
    permission_classes = [IsAuthor]
    queryset = Answer.objects.all()
    lookup_field = 'id'


class DestroyQuestionView(ModelViewSet):
    serializer_class = serializers.RetrieveQuestionSerializer
    permission_classes = [IsAuthor]
    queryset = Question.objects.all()
    lookup_field = 'id'


class CreateQuestionReview(ModelViewSet):
    serializer_class = serializers.QuestionReviewSerializer
    permission_classes = [IsAuthenticated]
    queryset = QuestionReview.objects.all()


class CreateAnswerReview(ModelViewSet):
    serializer_class = serializers.AnswerReviewSerializer
    permission_classes = [IsAuthenticated]
    queryset = AnswerReview.objects.all()