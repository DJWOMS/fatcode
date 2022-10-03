from rest_framework.permissions import BasePermission

from src.dashboard.models import Board
from src.repository.models import Project
from src.team.models import TeamMember


class IsAuthorProject(BasePermission):
    """ Is author of project """

    def has_permission(self, request, view):
        return Project.objects.filter(
            id=view.kwargs.get('project_id'), user=request.user
        ).exists()


class IsAuthorBoard(BasePermission):
    """ Is author of board """

    def has_permission(self, request, view):
        return Board.objects.filter(user=request.user).exists()


class IsMemberBoard(BasePermission):
    """ Is member of project """

    def has_object_permission(self, request, view, obj):
        return TeamMember.objects.filter(
            user=request.user, team=obj.column.board.project.team
        ).exists()


class IsMemberProject(BasePermission):
    """ Is member of project """

    def has_object_permission(self, request, view, obj):
        return TeamMember.objects.filter(user=request.user, team=obj.project.team).exists()

