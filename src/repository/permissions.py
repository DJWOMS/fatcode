from rest_framework.permissions import BasePermission

from src.repository.models import Project
from src.repository.services import get_my_repository
from src.team.permissions import is_author_of_team_for_project
from src.team.models import TeamMember

class ProjectPermission(BasePermission):
    def has_permission(self, request, view):
        if is_author_of_team_for_project(request):
            if not Project.objects.filter(repository=request.data['repository']).exists():
                if get_my_repository(request.data['repository'], request.user):
                    return True
        return False


class IsMemberTeam(BasePermission):
    """Только для автора или участника проекта"""

    def has_permission(self, request, view):
       return TeamMember.objects.filter(user=request.user, team__project_teams__id=view.kwargs.get('pk')).exists()