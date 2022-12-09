from rest_framework.permissions import BasePermission

from src.repository.models import Project
from src.repository.services import get_my_repository
from src.team.models import TeamMember


class IsMemberTeam(BasePermission):
    """Только для автора или участника проекта"""
    def has_permission(self, request, view):
       return TeamMember.objects.select_related('user').filter(user=request.user, team__project_teams__id=view.kwargs.get('pk')).exists()


class IsAuthorProject(BasePermission):
    """Только для автора проекта"""
    def has_permission(self, request, view):
        return Project.objects.select_related('user').filter(user=request.user, id=view.kwargs.get('pk')).exists()

