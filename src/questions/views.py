from . import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Question, Answer, QuestionReview, AnswerReview
from .permissions import IsAuthor
from ..base.classes import MixedSerializer, MixedPermissionSerializer


class ListQuestionsView(ModelViewSet):
    serializer_class = serializers.ListQuestionSerializer
    queryset = Question.objects.all()


class QuestionView(MixedPermissionSerializer, ModelViewSet):
    queryset = Question.objects.all()
    lookup_field = "id"
    serializer_classes_by_action = {
        "retrieve": serializers.RetrieveQuestionSerializer,
        "update": serializers.UpdateQuestionSerializer,
        "partial_update": serializers.UpdateQuestionSerializer,
        "destroy": serializers.RetrieveQuestionSerializer,
        "create": serializers.CreateQuestionSerializer,
    }
    permission_classes_by_action = {
        "create": (IsAuthenticated,),
        "update": (IsAuthor,),
        "retrieve": (AllowAny,),
        "partial_update": (IsAuthor,),
        "destroy": (IsAuthor,),
    }


class AnswerView(MixedSerializer, ModelViewSet):
    lookup_field = "id"
    queryset = Answer.objects.all()
    permission_classes = [IsAuthor]
    serializer_classes_by_action = {
        "update": serializers.UpdateAnswerSerializer,
        "destroy": serializers.AnswerSerializer,
        "partial_update": serializers.UpdateAnswerSerializer,
    }


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
