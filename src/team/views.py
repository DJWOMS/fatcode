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
                                  UpdateSocialLinkSerializer)
from src.team.permissions import IsAuthorOrReadOnly, IsMemberOfTeam, IsMemberOfTeam, OwnerTeam, AuthorOrMember
# TODO импортировать сериализаторы как serializer, уменьшить количество строк импорта


class SocialLinkView(MixedPermissionSerializer, viewsets.ModelViewSet):
    """CRUD социальной ссылке к команде"""
    permission_classes_by_action = {
        'list': (OwnerTeam, ),
        'retrieve': (OwnerTeam, ),
        'update': (OwnerTeam, ),
        'destroy': (OwnerTeam, )
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


class OwnTeamListView(MixedPermissionSerializer, viewsets.ModelViewSet):
    """Просморт команды где как создатель"""
    permission_classes_by_action = {
        'list': (OwnerTeam, ),
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
        'list': (AuthorOrMember, ),
        'retrieve': (AuthorOrMember, )
    }
    serializer_classes_by_action = {
        'list': TeamListSerializer,
        'retrieve': TeamRetrieveSerializer
    }

    def get_queryset(self):
        if self.action == 'list':
            return Team.objects.filter(members__user=self.request.user).exclude(user=self.request.user)
        elif self.action == 'retrieve':
            return Team.objects.filter(id=self.kwargs.get('pk'), teams__members_user=self.request.user)


class TeamView(MixedPermissionSerializer, viewsets.ModelViewSet):
    """Посмотреть/создать команду (CRUD)"""
    queryset = Team.objects.all()
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


class PostView(MixedPermissionSerializer, viewsets.ModelViewSet):
    """Создание поста если автор или дали такое право"""
    queryset = Post.objects.all().prefetch_related('post_comments')
    serializer_class = serializers.TeamPostSerializer
    permission_classes_by_action = {
        'list': (AuthorOrMember, ),
        'retrieve': (AuthorOrMember, ),
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
        if self.action == 'list':
            return Post.objects.filter(user=self.request.user)
        elif self.action == 'retrieve' or 'update' or 'destroy':
            return Post.objects.filter(id=self.kwargs.get('pk'))

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


class CommentsView(MixedPermissionSerializer, viewsets.ModelViewSet):
    """ CRUD комментариев к постам"""
    queryset = Comment.objects.all()
    serializer_class = serializers.TeamCommentCreateSerializer
    permission_classes_by_action = {
        'list': [AuthorOrMember],
        'create':  [AuthorOrMember],
        'update': [AuthorOrMember],
        'retrieve': [AuthorOrMember],
        'destroy': [AuthorOrMember]
    }

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, instance):
        instance.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()


class InvitationView(MixedPermissionSerializer, viewsets.ModelViewSet):
    """Создание/удаление заявки в команду"""
    permission_classes_by_action = {
        'list': [IsAuthenticatedOrReadOnly],
        'retrieve': [IsAuthenticatedOrReadOnly],
        'create': [IsAuthenticatedOrReadOnly],
        'destroy': [IsAuthorOrReadOnly]
    }
    serializer_classes_by_action = {
        'list': InvitationSerializer,
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
        'create': [IsAuthenticatedOrReadOnly],
        'destroy': [IsAuthenticatedOrReadOnly]
    }
    serializer_classes_by_action = {
        'list': AcceptInvitationSerializerList,
        'retrieve': AcceptInvitationSerializerList,
        'update': AcceptInvitationSerializer,
        'destroy': AcceptInvitationSerializer
    }

    def get_queryset(self):
        return Invitation.objects.filter(team__user=self.request.user, order_status='Waiting')

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()
