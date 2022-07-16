from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated


class DetailCourseView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = DetailCourseSerializer
    lookup_field = 'slug'


class ListCourseView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = ListCourseSerializer


class DetailLessonView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    lookup_field = 'slug'
    serializer_class = DetailLessonSerializer

