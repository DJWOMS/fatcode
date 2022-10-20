from django.db.models import Q
from rest_framework import generics, permissions, viewsets, parsers, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from src.base.permissions import IsAuthor
from . import permissions as perm
from src.base.classes import MixedSerializer, MixedPermission
from src.base.service import post_view_count
from src.team.models import Team, Post, Comment, TeamMember, Invitation, SocialLink
from src.team import serializers
from src.team.services import create_team_member
from src.team.serializers import (TeamSerializer,
                                  UpdateTeamSerializer,
                                  DetailTeamSerializer,
                                  TeamListSerializer,
                                  CreateTeamSerializer,
                                  ByUserTeamMemberSerializer,
                                  TeamRetrieveSerializer,
                                  CreatePost,
                                  InvitationAskingSerializer,
                                  InvitationSerializer)
from src.team.permissions import IsAuthor, OwnerTeam, IsMemberOfTeam


class OwnTeamListView(MixedPermission, viewsets.ModelViewSet):
    """Просморт команды где как создатель"""
    permission_classes_by_action = {'list': [IsAuthor],
                                    'get': [IsAuthor],
                                    'update': [IsAuthor],
                                    'destroy': [IsAuthor]}

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()

    def get_queryset(self):
        teams = Team.objects.filter(user=self.request.user)
        return teams

    def get_serializer_class(self):
        if self.action == 'list':
            return TeamListSerializer
        elif self.action == 'retrieve':
            return TeamRetrieveSerializer
        elif self.action == 'update' or 'destroy':
            return UpdateTeamSerializer


# почему не дает вывести 1 команду с этим участником
class MemberTeamListView(MixedPermission, viewsets.ModelViewSet):
    """Просморт команды где как участник"""
    permission_classes_by_action = {'list': [IsAuthenticated],
                                    'get': [IsMemberOfTeam],
                                    'update': [IsAuthenticated],
                                    'destroy': [IsAuthenticated]}

    def get_queryset(self):
        if self.action == 'list':
            teams = Team.objects.filter(members__user=self.request.user)
            print(teams)
            return teams
        # elif self.action == 'retrieve':
        #     print(self.kwargs.get('pk'))
        #     teams = Team.objects.filter(id=self.kwargs.get('pk'))
        #     print(teams)
        #     return teams

    def get_serializer_class(self):
        if self.action == 'list':
            return TeamListSerializer
        elif self.action == 'retrieve':
            return TeamRetrieveSerializer



class TeamView(MixedPermission, viewsets.ModelViewSet):
    """  Посмотреть/создать команду (CRUD)"""

    queryset = Team.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action == 'list' or 'retrieve':
            permission_classes = [IsAuthenticatedOrReadOnly]
            return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list':
            return TeamSerializer
        elif self.action == 'create':
            return CreateTeamSerializer
        elif self.action == 'retrieve':
            return DetailTeamSerializer

class PostView(MixedPermission, viewsets.ModelViewSet):
    """ Создание поста если автор или дали такое право """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all().prefetch_related('post_comments')
    serializer_class = serializers.TeamPostSerializer
    permission_classes_by_action = {
        'retrieve': [perm.IsMemberOfTeamForPost],
        'create': [perm.IsMemberOfTeam],
        'update': [IsAuthor],
        'destroy': [IsAuthor]
    }

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance = post_view_count(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        team = Team.objects.get(id=self.kwargs.get('pk'))
        serializer.save(team=team)

    def perform_update(self, instance):
        instance.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()

class PostsView(MixedPermission, viewsets.ModelViewSet):
    '''Просмотр постов для членов команды'''
    queryset = Post.objects.all()
    serializer_class = serializers.TeamPostSerializer
    permission_classes_by_action = {
        'list': [IsAuthenticatedOrReadOnly],
        'retrieve': [IsAuthenticatedOrReadOnly],
        'create': [IsAuthenticatedOrReadOnly],
        'update': [IsAuthor],
        'destroy': [IsAuthor]
    }

    def get_queryset(self):
        if self.action == 'list':
            posts = Post.objects.filter(user=self.request.user)
            return posts
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()

    def perform_update(self, instance):
        instance.save(user=self.request.user)

class CommentsView(MixedPermission, viewsets.ModelViewSet):
    """ CRUD комментариев к записи """
    queryset = Comment.objects.all()
    serializer_class = serializers.TeamCommentCreateSerializer
    permission_classes_by_action = {
        'list': [IsAuthenticatedOrReadOnly],
        'create':  [IsAuthenticatedOrReadOnly],
        'update': [IsAuthenticatedOrReadOnly],
        'retrieve': [IsAuthenticatedOrReadOnly],
        'destroy': [IsAuthenticatedOrReadOnly]
    }

    def get_queryset(self):
        if self.action == 'list':
            teams = TeamMember.objects.filter(user=self.request.user)
            print(teams)
            # posts = Post.objects.filter(team__articles=self.request.user)
            return teams

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, instance):
        instance.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()
#

class InvitationView(MixedPermission, viewsets.ModelViewSet):
    """ Создание/удаление заявки в команду"""
    queryset = Invitation.objects.all()
    permission_classes_by_action = {
        'list': [IsAuthenticatedOrReadOnly],
        'retrieve': [IsAuthenticatedOrReadOnly],
        'create': [IsAuthenticatedOrReadOnly],
        'destroy': [IsAuthor]
    }

    def get_queryset(self):
        invitation = Invitation.objects.filter(user=self.request.user)
        return invitation

    def get_serializer_class(self):
        if self.action == 'list':
            return InvitationSerializer
        elif self.action == 'create' or 'destroy':
            return InvitationAskingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()

#не доделано
class InvitationDetailView(MixedPermission, viewsets.ModelViewSet):
    """ Принять/отклонить заявки в команду"""
    queryset = Invitation.objects.all()
    permission_classes_by_action = {
        'list': [IsAuthenticatedOrReadOnly],
        'retrieve': [IsAuthenticatedOrReadOnly],
        'create': [IsAuthenticatedOrReadOnly],
        'destroy': [IsAuthor]
    }

    def get_queryset(self):
        invitation = Invitation.objects.filter(user=self.request.user, team__invitations__user=self.request.user)
        print(invitation)
        return invitation

    def get_serializer_class(self):
        if self.action == 'list':
            return InvitationSerializer
        elif self.action == 'create' or 'destroy':
            return InvitationAskingSerializer

    def perform_create(self, serializer):
        serializer.save(asking=False)

    def perform_destroy(self, instance):
        instance.delete()

#
# class TeamAvatarView(viewsets.ModelViewSet):
#     """ Updating team avatar """
#     queryset = Team.objects.all()
#     serializer_class = serializers.TeamAvatarSerializer
#     permission_classes = [permissions.IsAuthenticated, IsAuthor]
#     parser_classes = (parsers.MultiPartParser,)
#
#
# class TeamListByUserView(generics.ListAPIView):
#     """ Team list by user or which is member """
#     serializer_class = serializers.ByUserTeamListSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def list(self, request, *args, **kwargs):
#         owner = Team.objects.filter(user=self.request.user)
#         member = Team.objects.filter(members__user=self.request.user).exclude(user=self.request.user)
#
#         owner_serializer = self.get_serializer(owner, many=True)
#         member_serializer = self.get_serializer(member, many=True)
#         return Response({'owner': owner_serializer.data, 'member': member_serializer.data})
#
#
# class SocialLinkView(viewsets.ModelViewSet):
#     queryset = SocialLink.objects.all()
#     serializer_class = serializers.SocialLinkSerializer
#     permission_classes = [permissions.IsAuthenticated, perm.OwnerTeam]
# class TeamListView(generics.ListAPIView):
#     """Team list and search view"""
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = serializers.TeamListSerializer
#
#     def get_queryset(self):
#         # teams = Team.objects.exclude(Q(members__user=self.request.user) | Q(user=self.request.user))
#         teams = Team.objects.select_related('user').prefetch_related('members').all()
#         name = self.request.query_params.get('name')
#         user = self.request.query_params.get('user')
#
#         if name:
#             teams = Team.objects.filter(name__icontains=name)
#         if user:
#             teams = Team.objects.filter(user__username__icontains=user)
#         return teams

#
# class InvitationListView(generics.ListAPIView):
#     """Invitation to team member list view"""
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = serializers.InvitationListSerializer
#
#     def get_queryset(self):
#         return Invitation.objects.filter(
#             Q(user=self.request.user, asking=False) | Q(team__user=self.request.user, asking=False)
#         )
#
#
# class InvitationAskingListView(generics.ListAPIView):
#     """Request to team member list view"""
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = serializers.InvitationListSerializer
#
#     def get_queryset(self):
#         return Invitation.objects.filter(
#             Q(team__user=self.request.user, asking=True) | Q(user=self.request.user, asking=True)
#         )
#
#
# class InvitationCreateView(generics.CreateAPIView):
#     """ Invite user to team """
#     permission_classes = [permissions.IsAuthenticated, perm.IsAuthorOfTeam]
#     queryset = Invitation.objects.all()
#     serializer_class = serializers.InvitationSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(asking=False)
#
#
# class InvitationAskingView(MixedPermission, viewsets.ModelViewSet):
#     """ User request to team member"""
#     permission_classes = [permissions.IsAuthenticated]
#     queryset = Invitation.objects.all()
#     serializer_class = serializers.InvitationAskingSerializer
#     # serializer_action_classes = {'update': serializers.AcceptInvitationSerializer}
#     permission_classes_by_action = {
#         'create': [permissions.IsAuthenticated],
#         'destroy': [permissions.IsAuthenticated]
#     }
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#
# class AcceptInvitationView(generics.UpdateAPIView):
#     """ Accept Invitation to team member"""
#     queryset = Invitation.objects.all()
#     permission_classes = [permissions.IsAuthenticated, perm.IsInvitationToRequestUser]
#     serializer_class = serializers.AcceptInvitationSerializer
#
#     # def get_queryset(self):
#     #     return Invitation.objects.filter(id=self.kwargs['pk'])
#
#     def perform_update(self, serializer):
#         serializer.save()
#         create_team_member(self, serializer)
#
#
# class AcceptInvitationAskingView(MixedPermission, viewsets.ModelViewSet):
#     """ Accept user request to team member """
#     queryset = Invitation.objects.all()
#     permission_classes_by_action = {
#         "update": [
#             permissions.IsAuthenticated,
#             perm.IsInvitationAskingToAuthorOfTeam,
#             perm.IsAuthorOfTeamForInvitation
#         ],
#         "destroy": [perm.IsInvitationUser]
#     }
#     serializer_class = serializers.AcceptInvitationSerializer
#
#     def perform_update(self, serializer):
#         serializer.save()
#         create_team_member(self, serializer)
#
#
# class TeamMemberView(MixedPermission, viewsets.ModelViewSet):
#     """Retrieve and Destroy TeamMember view """
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     queryset = TeamMember.objects.all()
#     serializer_class = serializers.TeamMemberSerializer
#     permission_classes_by_action = {'destroy': [perm.IsAuthorOfTeamForDetail]}
#
#     def destroy(self, request, *args, **kwargs):
#         obj = get_object_or_404(TeamMember, user_id=self.kwargs['pk'], team_id=self.kwargs['team'])
#         self.check_object_permissions(self.request, obj)
#         self.perform_destroy(obj)
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# class TeamMemberSelfDeleteView(MixedPermission, viewsets.ModelViewSet):
#     """Self Destroy TeamMember view """
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     queryset = TeamMember.objects.all()
#     serializer_class = serializers.TeamMemberSerializer
#     permission_classes_by_action = {'destroy': [perm.IsNotAuthorOfTeamForSelfDelete]}
#
#     def destroy(self, request, *args, **kwargs):
#         obj = get_object_or_404(TeamMember, user=request.user, team_id=self.kwargs['team'])
#         self.check_object_permissions(self.request, obj)
#         self.perform_destroy(obj)
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# class TeamMemberListView(generics.ListAPIView):
#     """ TeamMember list view """
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = serializers.TeamMemberSerializer
#
#     def get_queryset(self):
#         return TeamMember.objects.filter(team_id=self.kwargs.get('pk'))
#
#
# class PostListView(generics.ListAPIView):
#     """ Список постов на стене команды"""
#     serializer_class = serializers.TeamListPostSerializer
#     permission_classes = [permissions.IsAuthenticated, perm.IsMemberOfTeam]
#
#     def get_queryset(self):
#         return Post.objects.filter(
#             team_id=self.kwargs.get('pk')
#         ).prefetch_related('post_comments')
#
#