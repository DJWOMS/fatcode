from django.db.models import Q
from rest_framework import generics, permissions, viewsets, parsers, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from src.base.permissions import IsAuthor
from . import permissions as perm
from src.base.classes import MixedSerializer, MixedPermission, MixedPermissionSerializer
from src.base.service import post_view_count
from src.team.models import Team, Post, Comment, TeamMember, Invitation, SocialLink
from src.team import serializers
from src.team.services import create_team_member
from src.team.serializers import (TeamSerializer,
                                  UpdateTeamSerializer,
                                  DetailTeamSerializer,
                                  TeamListSerializer,
                                  CreateTeamSerializer,
                                  TeamRetrieveSerializer,
                                  CreatePost,
                                  InvitationAskingSerializer,
                                  InvitationSerializer,
                                  AcceptInvitationSerializer,
                                  TeamMemberRetrieveSerializer,
                                  SocialLinkSerializer,
                                  CreateSocialLinkSerializer,
                                  ListSocialLinkSerializer,
                                  AcceptInvitationSerializerList,
                                  UpdateSocialLinkSerializer,
                                  TeamCommentUpdateSerializer,
                                  TeamUpdateSerializer)
from src.team.permissions import (IsAuthorOrReadOnly,
                                  IsMemberOfTeam,
                                  IsMemberOfTeam,
                                  OwnerTeam,
                                  AuthorOrMember,
                                  SocialOwnerTeam,
                                  MemberTeam,
                                  PostOwnerTeam,
                                  CommentOwnerTeam)


class SocialLinkView(MixedPermissionSerializer, viewsets.ModelViewSet):
    """CRUD социальной ссылке к команде"""
    permission_classes_by_action = {
        'list': (IsAuthenticatedOrReadOnly, ),
        'create': (IsAuthenticatedOrReadOnly, ),
        'retrieve': (SocialOwnerTeam, ),
        'update': (SocialOwnerTeam, ),
        'destroy': (SocialOwnerTeam, ),
    }
    serializer_classes_by_action = {
        'list': ListSocialLinkSerializer,
        'retrieve': ListSocialLinkSerializer,
        'create': CreateSocialLinkSerializer,
        'update': UpdateSocialLinkSerializer,
        'destroy': UpdateSocialLinkSerializer
    }

    def get_queryset(self):
        return SocialLink.objects.filter(team__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()

    def get_queryset(self):
        teams = SocialLink.objects.filter(team__user=self.request.user)
        return teams

    # def get_serializer_class(self):
    #     if self.action == 'list' or 'retrieve':
    #         return ListSocialLinkSerializer
    #     elif self.action == 'create':
    #         return CreateSocialLinkSerializer
    #     elif self.action == 'update' or 'destroy':
    #         return UpdateSocialLinkSerializer


class OwnTeamListView(MixedPermissionSerializer, viewsets.ModelViewSet):
    """Просморт команды где как создатель"""
    permission_classes_by_action = {
        'list': (IsAuthenticatedOrReadOnly, ),
        'retrieve': (OwnerTeam, ),
        'update': (OwnerTeam, ),
        'destroy': (OwnerTeam, )
    }
    serializer_classes_by_action = {
        'list': TeamListSerializer,
        'retrieve': TeamRetrieveSerializer,
        'update': UpdateTeamSerializer,
        'destroy': UpdateTeamSerializer
    }

    def get_queryset(self):
        return Team.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()


class MemberTeamListView(MixedPermissionSerializer, viewsets.ModelViewSet):
    """Просморт команды где как участник"""
    permission_classes_by_action = {
        'list': (IsAuthenticatedOrReadOnly, ),
        'retrieve': (MemberTeam, )
    }
    serializer_classes_by_action = {
        'list': TeamListSerializer,
        'retrieve': TeamRetrieveSerializer
    }

    def get_queryset(self):
        return Team.objects.filter(members__user=self.request.user).exclude(user=self.request.user)


class TeamView(MixedSerializer, viewsets.ModelViewSet):
    """  Посмотреть/создать команду (CRUD)"""
    queryset = Team.objects.all()
    permission_classes = IsAuthenticatedOrReadOnly
    serializer_classes_by_action = {
        'list': TeamSerializer,
        'retrieve': DetailTeamSerializer,
        'create': CreateTeamSerializer
    }

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action == 'list' or 'retrieve':
            permission_classes = [IsAuthenticatedOrReadOnly]
            return [permission() for permission in permission_classes]


class ShowPostsView(MixedPermission, viewsets.ModelViewSet):
    """ Просмотр постов как участник """
    serializer_class = serializers.TeamListPostSerializer
    permission_classes_by_action = {
        'list': (IsAuthenticatedOrReadOnly, ),
        'retrieve': (PostOwnerTeam, ),
    }

    def get_queryset(self):
        posts = Post.objects.filter(team__members__user=self.request.user).prefetch_related('post_comments')
        return posts


class PostView(MixedPermissionSerializer, viewsets.ModelViewSet):
    """ Создание поста если автор или дали такое право """
    serializer_class = serializers.TeamListPostSerializer
    serializer_classes_by_action = {
        'list': serializers.TeamListPostSerializer,
        'retrieve': serializers.TeamListPostSerializer,
        'create': serializers.TeamPostSerializer,
        'update': TeamUpdateSerializer,
        'destroy': TeamUpdateSerializer
    }
    permission_classes_by_action = {
        'list': (IsAuthenticatedOrReadOnly, ),
        'retrieve': (IsAuthenticatedOrReadOnly, ),
        'create': (OwnerTeam, ),
        'update': (OwnerTeam, ),
        'destroy': (OwnerTeam, ),
    }
    serializer_classes_by_action = {
        'list': serializers.TeamPostSerializer,
        'retrieve': serializers.TeamPostSerializer,
        'create': serializers.TeamPostSerializer,
        'update': serializers.TeamPostSerializer,
        'destroy': serializers.TeamPostSerializer,
    }

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance = post_view_count(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()

    def perform_update(self, instance):
        instance.save(user=self.request.user, id=self.kwargs.get('pk'))


class CommentsViewOwn(MixedPermissionSerializer, viewsets.ModelViewSet):
    """ CRUD комментариев к постам как автор команды"""

    permission_classes_by_action = {
        'list': (IsAuthenticatedOrReadOnly, ),
        'retrieve': (CommentOwnerTeam, ),
        'destroy': (CommentOwnerTeam, )
    }
    serializer_classes_by_action = {
        'list': serializers.TeamCommentListSerializer,
        'retrieve': serializers.TeamCommentListSerializer,
        'destroy': TeamCommentUpdateSerializer
    }

    def get_queryset(self):
        return Comment.objects.filter(post__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, instance):
        instance.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()


class CommentsView(MixedPermissionSerializer, viewsets.ModelViewSet):
    """ CRUD комментариев к постам как участник"""

    permission_classes_by_action = {
        'list': (IsAuthenticatedOrReadOnly, ),
        'create':  (IsAuthenticatedOrReadOnly, ),
        'update': (OwnerTeam, ),
        'retrieve': (IsAuthenticatedOrReadOnly, ),
        'destroy': (OwnerTeam, )
    }
    serializer_classes_by_action = {
        'list': serializers.TeamCommentListSerializer,
        'create': serializers.TeamCommentCreateSerializer,
        'retrieve': serializers.TeamCommentListSerializer,
        'update': TeamCommentUpdateSerializer,
        'destroy': TeamCommentUpdateSerializer
    }

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, instance):
        instance.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()


class InvitationView(MixedPermissionSerializer, viewsets.ModelViewSet):
    """Создание/удаление заявки в команду"""
    permission_classes_by_action = {
        'list': (IsAuthenticatedOrReadOnly, ),
        'retrieve': (OwnerTeam, ),
        'create': (IsAuthenticatedOrReadOnly, ),
        'destroy': (OwnerTeam, )
    }
    serializer_classes_by_action = {
        'list': InvitationSerializer,
        'retrieve': InvitationSerializer,
        'create': InvitationAskingSerializer,
        'destroy': InvitationAskingSerializer
    }

    def get_queryset(self):
        return Invitation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()


class InvitationDetailView(MixedPermissionSerializer, viewsets.ModelViewSet):
    """ Принять/отклонить заявки в команду"""
    permission_classes_by_action = {
        'list': [IsAuthenticatedOrReadOnly],
        'retrieve': [IsAuthenticatedOrReadOnly],
        'update': [IsAuthenticatedOrReadOnly],
        'destroy': [IsAuthenticatedOrReadOnly]
    }
    serializer_classes_by_action = {
        'list': AcceptInvitationSerializerList,
        'retrieve': AcceptInvitationSerializerList,
        'update': AcceptInvitationSerializer,
        'destroy': AcceptInvitationSerializer
    }

    def get_queryset(self):
        invitation = Invitation.objects.filter(team__user=self.request.user, order_status='Waiting')
        print(invitation)
        return invitation

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()
