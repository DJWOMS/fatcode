from django.db.models import Q
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework import permissions
from src.team.models import Team, TeamMember, Invitation, Post


class IsAuthorOrReadOnly(permissions.BasePermission):
    '''Только для автора обьекта или просмотр'''
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsAuthor(permissions.BasePermission):
    '''Только для автора обьекта'''
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAuthorTeamForInvitation(permissions.BasePermission):
    '''Только для автора команды прием/отклонение заявок'''
    def has_object_permission(self, request, view, obj):
        team = Team.objects.get(name=obj.team)
        return team.user == request.user


class OwnerRetrieveDelete(permissions.BasePermission):
    '''Только для автора команды или просмотр'''

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            user = Team.objects.get(user=request.user, id=view.kwargs.get('pk'))
            return user.user == request.user
        except Team.DoesNotExist:
            return False

class MemberTeam(permissions.BasePermission):
    '''Только для автора или участника'''

    def has_permission(self, request, view):
        try:
            user = TeamMember.objects.get(user=request.user, team_id=view.kwargs.get('pk'))
            return user.user == request.user
        except TeamMember.DoesNotExist:
            return False


def is_author_of_team_for_project(request):
    """ Is Author of team for creating a project """
    return Team.objects.filter(id=request.data['teams'], user=request.user)

