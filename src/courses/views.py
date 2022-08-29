from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from django_filters.rest_framework import DjangoFilterBackend

from .filters import CourseFilter
from .models import Course, Lesson, StudentWork, HelpUser
from .serializers import CourseSerializer, LessonSerializer, StudentWorkSerializer, HelpUserSerializer


class CourseModelView(ModelViewSet):
    """Courses"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend]
    lookup_field = 'id'
    filterset_class = CourseFilter

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class LessonModelView(ModelViewSet):
    """Detail lesson"""
    queryset = Lesson.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer


class StudentWorkView(ModelViewSet):
    """Student work"""
    queryset = StudentWork.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = StudentWorkSerializer


class HelpUserView(ModelViewSet):
    """Help user"""
    queryset = HelpUser.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = HelpUserSerializer
