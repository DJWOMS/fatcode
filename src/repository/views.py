from django.db.models import Q
from rest_framework import generics, viewsets, permissions
from django_filters import rest_framework as filters

from . import serializers, models
from .filters import ProjectFilter
from .permissions import IsMemberTeam

from ..base.classes import MixedSerializer, MixedPermissionSerializer
from ..base.permissions import IsUser
from ..team.models import Team
from ..dashboard.models import Board

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
    permission_classes_by_action = {
        'create': (permissions.IsAuthenticated, ),
        'list': (permissions.IsAuthenticated,)
    }
    serializer_classes_by_action = {
        'create': serializers.ProjectSerializer,
        'list': serializers.ProjectUserListSerializer,
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

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()


class MemberProjectTeamsView(MixedPermissionSerializer, viewsets.ModelViewSet):
    """Список команд проекта, если ты участник команды"""
    permission_classes_by_action = {
        'list': (IsMemberTeam,)
    }
    serializer_classes_by_action = {
        'list': serializers.ProjectTeamsSerializer
    }

    def get_queryset(self):
        return Team.objects.filter(project_teams=self.kwargs.get('pk'))


class MemberProjectBoardView(MixedPermissionSerializer, viewsets.ModelViewSet):
    """Доска задач проекта, если ты участник команды"""
    permission_classes_by_action = {
        'list': (IsMemberTeam,)
    }
    serializer_classes_by_action = {
        'list': serializers.ProjectTeamsSerializer
    }

    def get_queryset(self):
        return Board.objects.filter(project=self.kwargs.get('pk'))