from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from .models import Course, Lesson, StudentWork, HelpUser
from . import serializers
from rest_framework.permissions import IsAuthenticated
from .filters import CourseFilter
from django_filters.rest_framework import DjangoFilterBackend


class DetailCourseView(RetrieveAPIView):
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.DetailCourseSerializer
    lookup_field = 'id'


class ListCourseView(ListAPIView):
    queryset = Course.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseFilter
    serializer_class = serializers.ListCourseSerializer


class DetailLessonView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.DetailLessonSerializer


class StudentWorkView(CreateAPIView):
    queryset = StudentWork.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.StudentWorkSerializer


class HelpUserView(CreateAPIView):
    queryset = HelpUser
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.HelpUserSerializer
