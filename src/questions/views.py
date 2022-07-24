from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from . import serializers
from .models import Question


class ListQuestionsView(ListAPIView):
    serializer_class = serializers.ListQuestionSerializer
    queryset = Question.objects.all()


class RetrieveQuestionView(RetrieveAPIView):
    serializer_class = serializers.RetrieveQuestionSerializer
    queryset = Question.objects.all()
    lookup_field = 'id'


