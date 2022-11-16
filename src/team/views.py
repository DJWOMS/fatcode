from rest_framework import viewsets, status
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from django_filters import rest_framework as filters

from src.base.classes import MixedSerializer, MixedPermission, MixedPermissionSerializer
from src.base.service import post_view_count
from src.base.permissions import IsUser
from src.team import serializers, permissions, filters, models
from django_filters import rest_framework as filter


class TeamView(MixedPermissionSerializer, viewsets.ModelViewSet):
    """  Посмотреть/создать команду (CRUD)"""
    filterset_class = filters.TeamFilter
    filter_backends = (filter.DjangoFilterBackend,)
    queryset = models.Team.objects.prefetch_related('project_teams').select_related('user').all()
    permission_classes_by_action = {
        'list': (IsAuthenticatedOrReadOnly,),
        'create': (IsAuthenticated,),
        'retrieve': (IsAuthenticatedOrReadOnly,),
        'update': (IsUser, ),
        'destroy': (IsUser, )
    }
    serializer_classes_by_action = {
        'list': serializers.TeamSerializer,
        'retrieve': serializers.DetailTeamSerializer,
        'create': serializers.CreateTeamSerializer,
        'update': serializers.UpdateTeamSerializer,
        'destroy': serializers.UpdateTeamSerializer
    }

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()


class SocialLinkView(MixedPermissionSerializer, viewsets.ModelViewSet):
    """CRUD социальной ссылке к команде"""
    permission_classes_by_action = {
        'list': (IsAuthenticatedOrReadOnly, ),
        'create': (permissions.IsAuthorTeam, ),
        'retrieve': (permissions.IsAuthorTeamOrRead, ),
        'update': (permissions.IsAuthorTeam, ),
        'destroy': (permissions.IsAuthorTeam, ),
    }
    serializer_classes_by_action = {
        'list': serializers.ListSocialLinkSerializer,
        'retrieve': serializers.ListSocialLinkSerializer,
        'create': serializers.CreateSocialLinkSerializer,
        'update': serializers.UpdateSocialLinkSerializer,
        'destroy': serializers.UpdateSocialLinkSerializer
    }
    lookup_url_kwarg = 'social_pk'

    def get_queryset(self):
        return models.SocialLink.objects.select_related('team').filter(team=self.kwargs.get('pk'))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, team_id=self.kwargs.get('pk'))

    def perform_update(self, serializer):
        serializer.save(user=self.request.user, social_pk=self.kwargs.get('social_pk'))

    def perform_destroy(self, instance):
        instance.delete()


class OwnTeamListView(MixedPermissionSerializer, viewsets.ModelViewSet):
    """Просморт команды где как создатель"""
    permission_classes_by_action = {
        'list': (IsAuthenticated, )
    }
    serializer_classes_by_action = {
        'list': serializers.TeamListSerializer
    }

    def get_queryset(self):
        return models.Team.objects.select_related('user').prefetch_related('social_links')\
            .filter(user=self.request.user)


class MemberTeamListView(MixedPermissionSerializer, viewsets.ModelViewSet):
    """Просморт команд где как участник"""
    permission_classes_by_action = {
        'list': (IsAuthenticated, ),
    }
    serializer_classes_by_action = {
        'list': serializers.TeamListSerializer,
    }

    def get_queryset(self):
        return models.Team.objects.select_related('user').filter(members__user=self.request.user).exclude(user=self.request.user)


class MemberList(MixedPermissionSerializer, viewsets.ModelViewSet):
    """ Просмотр участников команды"""
    permission_classes_by_action = {
        'list': (permissions.IsMemberTeam, ),
        'retrieve': (permissions.IsMemberTeam, ),
        'destroy': (permissions.IsAuthorTeam, )
    }
    serializer_classes_by_action = {
        'list': serializers.MemberSerializer,
        'retrieve': serializers.MemberSerializer,
        'destroy': serializers.MemberSerializer
    }
    lookup_url_kwarg = 'member_pk'

    def get_queryset(self):
        return models.TeamMember.objects.prefetch_related('user').filter(team=self.kwargs.get('pk'))

    def perform_destroy(self, instance):
        if models.Team.objects.filter(name=instance.team, user=instance.user).exists():
            raise APIException(
                detail='Невозможно удалить себя из команды',
                code=status.HTTP_400_BAD_REQUEST
            )
        instance.delete()


class PostView(MixedPermissionSerializer, viewsets.ModelViewSet):
    """ CRUD поста если автор или дали такое право """
    serializer_classes_by_action = {
        'list': serializers.PostSerializer,
        'retrieve': serializers.PostSerializer,
        'create': serializers.PostCreateSerializer,
        'update': serializers.PostCreateSerializer,
        'destroy': serializers.PostCreateSerializer
    }
    permission_classes_by_action = {
        'list': (permissions.IsMemberTeam, ),
        'retrieve': (permissions.IsMemberTeam, ),
        'create': (permissions.IsAuthorTeam, ),
        'update': (IsUser, ),
        'destroy': (IsUser, ),
    }
    lookup_url_kwarg = 'post_pk'

    def get_queryset(self):
        return models.Post.objects.select_related('team', 'user').filter(team_id=self.kwargs.get('pk'))

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance = post_view_count(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        team_id=self.kwargs.get('pk'))

    def perform_destroy(self, instance):
        instance.delete()

    def perform_update(self, serializer):
        serializer.save(user=self.request.user, id=self.kwargs.get('post_pk'))


class CommentsView(MixedPermissionSerializer, viewsets.ModelViewSet):
    """CRUD комментариев к постам"""
    permission_classes_by_action = {
        'list': (permissions.IsMemberTeam, ),
        'create':  (permissions.IsMemberTeam, ),
        'update': (IsUser, ),
        'retrieve': (permissions.IsMemberTeam, ),
        'destroy': (IsUser, )
    }
    serializer_classes_by_action = {
        'list': serializers.CommentListSerializer,
        'create': serializers.CommentCreateSerializer,
        'retrieve': serializers.CommentListSerializer,
        'update': serializers.TeamCommentUpdateSerializer,
        'destroy': serializers.TeamCommentUpdateSerializer
    }
    lookup_url_kwarg = 'comment_pk'

    def get_queryset(self):
        return models.Comment.objects.select_related('post').filter(post_id=self.kwargs.get('post_pk'))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, post_id=self.kwargs.get('post_pk'))

    def perform_update(self, serializer):
        serializer.save(user=self.request.user, id=self.kwargs.get('comment_pk'))

    def perform_destroy(self, instance):
        instance.delete()


class InvitationView(MixedPermissionSerializer, viewsets.ModelViewSet):
    """CD заявки в команду"""
    permission_classes_by_action = {
        'list': (IsAuthenticated, ),
        'retrieve': (IsUser, ),
        'create': (IsAuthenticated, ),
        'destroy': (IsUser, )
    }
    serializer_classes_by_action = {
        'list': serializers.InvitationSerializer,
        'retrieve': serializers.InvitationSerializer,
        'create': serializers.InvitationAskingSerializer,
        'destroy': serializers.InvitationAskingSerializer
    }

    def get_queryset(self):
        return models.Invitation.objects.select_related('team', 'user').filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()


class InvitationDetailView(MixedPermissionSerializer, viewsets.ModelViewSet):
    """ Принять/отклонить заявки в команду"""
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'retrieve': (permissions.IsAuthorTeamForInvitation, ),
        'update': (permissions.IsAuthorTeamForInvitation, ),
    }
    serializer_classes_by_action = {
        'list': serializers.AcceptInvitationSerializerList,
        'retrieve': serializers.AcceptInvitationSerializerList,
        'update': serializers.AcceptInvitationSerializer,
    }

    def get_queryset(self):
        return models.Invitation.objects.select_related('team', 'user').filter(
                                                                                team__user=self.request.user,
                                                                                order_status='Waiting'
                                                                                )

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


