from . import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Question, Answer, QuestionReview, AnswerReview
from .permissions import IsAuthor


class ListQuestionsView(ModelViewSet):
    serializer_class = serializers.ListQuestionSerializer
    queryset = Question.objects.all()


class QuestionView(ModelViewSet):
    queryset = Question.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        serializer_class = {
            'retrieve': serializers.RetrieveQuestionSerializer,
            'update': serializers.UpdateQuestionSerializer,
            'partial_update': serializers.UpdateQuestionSerializer,
            'destroy': serializers.RetrieveQuestionSerializer
        }
        return serializer_class[self.action]

    def get_permissions(self):
        permission_class = {
            'create': IsAuthenticated,
            'update': IsAuthor,
            'retrieve': AllowAny,
            'partial_update': IsAuthor,
            'destroy': IsAuthor
        }
        self.permission_classes = [permission_class[self.action]]
        return super(QuestionView, self).get_permissions()


class AnswerView(ModelViewSet):
    lookup_field = 'id'
    queryset = Answer.objects.all()

    def get_permissions(self):
        permissions = {
            'update': IsAuthor,
            'partial_update': IsAuthor,
            'destroy': IsAuthor
        }
        self.permission_classes = [permissions[self.action]]
        return super(AnswerView, self).get_permissions()

    def get_serializer_class(self):
        serializer_classes = {
            'update': serializers.UpdateAnswerSerializer,
            'destroy': serializers.AnswerSerializer,
            'partial_update': serializers.UpdateAnswerSerializer,
        }
        return serializer_classes[self.action]


class CreateAnswerView(ModelViewSet):
    serializer_class = serializers.AnswerSerializer
    permission_classes = [IsAuthenticated]
    queryset = Answer.objects.all()


class CreateQuestionReview(ModelViewSet):
    serializer_class = serializers.QuestionReviewSerializer
    permission_classes = [IsAuthenticated]
    queryset = QuestionReview.objects.all()


class CreateAnswerReview(ModelViewSet):
    serializer_class = serializers.AnswerReviewSerializer
    permission_classes = [IsAuthenticated]
    queryset = AnswerReview.objects.all()


