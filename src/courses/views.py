from django.db.models import Q, OuterRef
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from ..base import classes

from . import serializers, models
from .filters import CourseFilter


class CategoryView(ReadOnlyModelViewSet):
    """Представление категорий"""
    serializer_class = serializers.CategoryChildrenSerializer

    def get_queryset(self):
        return models.Category.objects.prefetch_related('children').filter(parent__isnull=True)


class TagView(ReadOnlyModelViewSet):
    """Представлениетегов"""
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer


class CourseView(classes.MixedPermissionSerializer, ModelViewSet):
    """CRUD курсов"""
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseFilter
    serializer_classes_by_action = {
        "create": serializers.CourseSerializer,
        "update": serializers.CourseSerializer,
        "destroy": serializers.CourseSerializer,
        "list": serializers.ListCourseSerializer,
        "retrieve": serializers.CourseSerializer,
    }
    permission_classes_by_action = {
        "create": (IsAdminUser,),
        "update": (IsAdminUser,),
        "destroy": (IsAdminUser,),
        "list": (AllowAny,),
        "retrieve": (IsAuthenticated,)
    }

    def get_queryset(self):
        return (
            models.Course.objects
            .select_related('author', 'category', 'mentor')
            .prefetch_related('students', 'tags')
            .all()
        )


class LessonView(classes.MixedPermissionSerializer, ModelViewSet):
    """CRUD уроков"""
    queryset = models.Lesson.objects.select_related('course').all()
    serializer_classes_by_action = {
        "create": serializers.LessonDetailSerializer,
        "update": serializers.LessonDetailSerializer,
        "destroy": serializers.LessonDetailSerializer,
        "list": serializers.LessonListSerializer,
        "retrieve": serializers.LessonDetailSerializer,
    }
    permission_classes_by_action = {
        "create": (IsAdminUser,),
        "update": (IsAdminUser,),
        "destroy": (IsAdminUser,),
        "retrieve": (IsAuthenticated,),
        "list": (AllowAny,)
    }


class StudentWorkView(CreateAPIView):
    """Создание студентов"""
    queryset = models.StudentWork.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.StudentWorkSerializer


class HelpUserView(CreateAPIView):
    """Помощь пользователям"""
    queryset = models.HelpUser
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.HelpUserSerializer
