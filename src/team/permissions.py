from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework import permissions
from src.team.models import Team, TeamMember, Invitation


class IsAuthor(permissions.BasePermission):
    '''Редактирование для автора или только чтение'''
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user)

class OwnerTeam(BasePermission):
    def has_permission(self, request, view):
        if view.request.data.get('team'):
            return Team.objects.filter(
                id=view.request.data.get('team'),
                user=request.user
            ).exists()

    def has_object_permission(self, request, view, obj):
        return bool(obj.team.user == request.user)


class IsAuthorOfTeam(BasePermission):
    """ Is Author of team """

    def has_permission(self, request, view):
        if view.request.data.get('team'):
            return Team.objects.filter(
                id=view.request.data.get('team'),
                user=request.user
            ).exists()


def is_author_of_team_for_project(request):
    """ Is Author of team for creating a project """
    return Team.objects.filter(id=request.data['teams'], user=request.user)


class IsAuthorOfTeamForDetail(BasePermission):
    """ Is Author of team for team detail view """

    def has_object_permission(self, request, view, obj):
        return Team.objects.filter(
            id=view.kwargs['team'],
            user=request.user,
            #members__id=view.kwargs['pk']
        ).exists() and not obj.user == request.user


class IsNotAuthorOfTeamForSelfDelete(BasePermission):
    """ Is NOT Author of team for self delete from team """

    def has_object_permission(self, request, view, obj):
        return not Team.objects.filter(
            id=view.kwargs['team'],
            user=request.user,
        ).exists() and obj.user == request.user


class IsAuthorOfTeamForInvitation(BasePermission):
    """ Is Author of team for team invitation """

    def has_object_permission(self, request, view, obj):
        return Team.objects.filter(
            id=obj.team.id,
            user=request.user,
        ).exists() and not obj.user == request.user


class IsMemberOfTeam(BasePermission):
    """ Если член команды """

    def has_permission(self, request, view):
        if view.request.data.get('team'):
            return TeamMember.objects.filter(
                team_id=view.request.data.get('team'),
                user=request.user
            ).exists()
        else:
            return TeamMember.objects.filter(
                team_id=view.kwargs['pk'],
                user=request.user
            ).exists()


class IsMemberOfTeamForPost(BasePermission):
    """ Is member of team for team post """

    def has_object_permission(self, request, view, obj):
        return TeamMember.objects.filter(
            team_id=obj.team.id,
            user=request.user
        ).exists()


class IsMemberOfTeamForComment(BasePermission):
    """ Is member of team for team comment """

    def has_permission(self, request, view):
        if view.request.data.get('post'):
            return TeamMember.objects.filter(
                team__articles=view.request.data.get('post'),
                user=request.user
            ).exists()


class IsInvitationToRequestUser(BasePermission):
    """ Is Invitation to request user """

    def has_object_permission(self, request, view, obj):
        return Invitation.objects.filter(
            id=obj.id,
            user=request.user,
            asking=False
        ).exists()


class IsInvitationUser(IsAuthenticated):
    """ Is Invitation to request user """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsInvitationAskingToAuthorOfTeam(BasePermission):
    """ Is request to team member to request user """

    def has_object_permission(self, request, view, obj):
        return Invitation.objects.filter(
            id=obj.id,
            asking=True
        ).exists()


class PostPermission(BasePermission):
    """ Is request to team member to request user """

    def has_object_permission(self, request, view, obj):
        return Invitation.objects.filter(
            id=obj.id,
            asking=True
        ).exists()
