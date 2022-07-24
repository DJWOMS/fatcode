from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from .models import Course, Lesson, StudentWork, HelpUser
from .serializers import (
    DetailCourseSerializer,
    ListCourseSerializer,
    DetailLessonSerializer,
    StudentWorkSerializer,
    HelpUserSerializer
)
from rest_framework.permissions import IsAuthenticated


class DetailCourseView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = DetailCourseSerializer
    lookup_field = 'id'


class ListCourseView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = ListCourseSerializer


class DetailLessonView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    serializer_class = DetailLessonSerializer


class StudentWorkView(CreateAPIView):
    queryset = StudentWork.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = StudentWorkSerializer


class HelpUserView(CreateAPIView):
    queryset = HelpUser
    permission_classes = [IsAuthenticated]
    serializer_class = HelpUserSerializer
