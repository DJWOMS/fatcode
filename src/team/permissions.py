from django.db.models import Q
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework import permissions
from src.team.models import Team, TeamMember, Invitation, Post


class IsAuthor(permissions.BasePermission):
    """Только для автора обьекта"""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAuthorTeamForInvitation(permissions.BasePermission):
    """Только для автора команды прием/отклонение заявок"""
    def has_object_permission(self, request, view, obj):
        return obj.team.user == request.user


class IsAuthorTeamOrRead(permissions.BasePermission):
    """Только для автора команды или просмотр"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return Team.objects.filter(user=request.user, id=view.kwargs.get('pk')).exists()


class IsAuthorTeam(permissions.BasePermission):
    """Только для автора команды"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return Team.objects.filter(user=request.user, id=view.kwargs.get('pk')).exists()


class IsMemberTeam(permissions.BasePermission):
    """Только для автора или участника"""

    def has_permission(self, request, view):
        return TeamMember.objects.filter(user=request.user, team__id=view.kwargs.get('pk')).exists()


##TODO подумать над permission
def is_author_of_team_for_project(request):
    """ Is Author of team for creating a project """
    return Team.objects.filter(id=request.data['teams'], user=request.user)

