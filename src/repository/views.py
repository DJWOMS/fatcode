from rest_framework import generics, viewsets, permissions
from django_filters import rest_framework as filters

from . import serializers, models
from .filters import ProjectFilter
from .permissions import IsMemberTeam

from ..base.classes import MixedPermissionSerializer
from ..base.permissions import IsUser
from ..team.models import Team
from ..dashboard.models import Board


class CategoryListView(generics.ListAPIView):
    queryset = models.Category.objects.prefetch_related('projects').all()
    serializer_class = serializers.CategorySerializer


class ToolkitListView(generics.ListAPIView):
    queryset = models.Toolkit.objects.prefetch_related('projects').all()
    serializer_class = serializers.ToolkitSerializer


class ProjectsView(MixedPermissionSerializer, viewsets.ModelViewSet):
    """CRUD проекта"""
    permission_classes_by_action = {
        'list': (permissions.IsAuthenticated,),
        'retrieve': (permissions.IsAuthenticated,),
        'create': (permissions.IsAuthenticated,),
        'update': (IsUser,),
        'destroy': (IsUser,)
    }
    filterset_class = ProjectFilter
    filter_backends = (filters.DjangoFilterBackend,)
    serializer_classes_by_action = {
        'list': serializers.ProjectUserListSerializer,
        'retrieve': serializers.ProjectDetailSerializer,
        'create': serializers.ProjectSerializer,
        'update': serializers.ProjectSerializer,
        'destroy': serializers.ProjectSerializer
    }

    def get_queryset(self):
        project = models.Project.objects.select_related('user', 'category').all().prefetch_related('toolkit', 'teams')
        return project

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save(pk=self.kwargs.get('pk'))

    def perform_destroy(self, instance):
        instance.delete()


class UserProjectsView(MixedPermissionSerializer, viewsets.ModelViewSet):
    """Список проектов пользователя"""
    permission_classes_by_action = {
        'list': (permissions.IsAuthenticated,)
    }
    serializer_classes_by_action = {
        'list': serializers.ProjectUserListSerializer,
    }

    def get_queryset(self):
        return models.Project.objects.select_related('user', 'category').prefetch_related('toolkit', 'teams').\
            filter(user=self.request.user)


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
        return Board.objects.select_related('board').filter(project=self.kwargs.get('pk'))