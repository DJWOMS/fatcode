from django.db.models import Q
from rest_framework import generics, viewsets, permissions
from django_filters import rest_framework as filters

from . import serializers, models
from .filters import ProjectFilter
from .permissions import ProjectPermission

from ..base.classes import MixedSerializer, MixedPermissionSerializer
from ..base.permissions import IsUser


class CategoryListView(generics.ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class ToolkitListView(generics.ListAPIView):
    queryset = models.Toolkit.objects.all()
    serializer_class = serializers.ToolkitSerializer


class ProjectsView(MixedSerializer, viewsets.ReadOnlyModelViewSet):
    queryset = (
        models.Project.objects
        .select_related('user', 'category')
        .prefetch_related('toolkit', 'teams')
        .all()
    )
    filterset_class = ProjectFilter
    filter_backends = (filters.DjangoFilterBackend,)
    serializer_classes_by_action = {
        'list': serializers.ProjectListSerializer,
        'retrieve': serializers.ProjectDetailSerializer
    }


class UserProjectsView(MixedPermissionSerializer, viewsets.ModelViewSet):
    permission_classes = (IsUser,)
    permission_classes_by_action = {'create': (permissions.IsAuthenticated, ProjectPermission)}
    serializer_classes_by_action = {
        'create': serializers.ProjectSerializer,
        'list': serializers.ProjectListSerializer,
        'retrieve': serializers.ProjectDetailSerializer,
        'update': serializers.ProjectSerializer,
        'destroy': serializers.ProjectSerializer
    }

    def get_queryset(self):
        return (
            models.Project.objects
            .select_related('user', 'category')
            .prefetch_related('toolkit', 'teams')
            .filter(Q(user=self.request.user) | Q(teams__members__user=self.request.user)).distinct()
            .all()
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
