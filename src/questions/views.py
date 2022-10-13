from . import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Question, Answer, QuestionReview, AnswerReview
from ..base.permissions import IsAuthor
from ..base.classes import MixedPermissionSerializer


class QuestionView(MixedPermissionSerializer, ModelViewSet):
    queryset = Question.objects.all()
    lookup_field = "id"
    serializer_classes_by_action = {
        "list": serializers.ListQuestionSerializer,
        "retrieve": serializers.RetrieveQuestionSerializer,
        "update": serializers.UpdateQuestionSerializer,
        "partial_update": serializers.UpdateQuestionSerializer,
        "destroy": serializers.RetrieveQuestionSerializer,
        "create": serializers.CreateQuestionSerializer,
    }
    permission_classes_by_action = {
        "create": (IsAuthenticated,),
        "list": (AllowAny,),
        "update": (IsAuthor,),
        "retrieve": (AllowAny,),
        "partial_update": (IsAuthor,),
        "destroy": (IsAuthor,),
    }

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AnswerView(MixedPermissionSerializer, ModelViewSet):
    lookup_field = "id"
    queryset = Answer.objects.all()
    permission_classes = (IsAuthor,)
    permission_classes_by_action = {
        "create": (IsAuthenticated,)
    }
    serializer_classes_by_action = {
        "create": serializers.AnswerSerializer,
        "update": serializers.UpdateAnswerSerializer,
        "destroy": serializers.AnswerSerializer,
        "partial_update": serializers.UpdateAnswerSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CreateQuestionReview(ModelViewSet):
    serializer_class = serializers.QuestionReviewSerializer
    permission_classes = (IsAuthenticated,)
    queryset = QuestionReview.objects.all()


class CreateAnswerReview(ModelViewSet):
    serializer_class = serializers.AnswerReviewSerializer
    permission_classes = (IsAuthenticated,)
    queryset = AnswerReview.objects.all()
