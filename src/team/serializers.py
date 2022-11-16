from django.db.models import Q
from rest_framework import serializers, status
from rest_framework.exceptions import APIException

from ..base.exceptions import CustomException
from ..base.serializers import FilterCommentListSerializer
from .models import Post, Comment, Team, TeamMember, Invitation, SocialLink
from ..profiles.serializers import GetUserSerializer
from src.repository.models import Project


class TeamNameView(serializers.ModelSerializer):
    """Вывод команды при добавлении социальной ссылки"""

    class Meta:
        model = Team
        fields = ('name',)


class ListSocialLinkSerializer(serializers.ModelSerializer):
    """Просмотр социальных сетей'"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SocialLink
        fields = ('id', 'name', 'link', 'user')


class UpdateSocialLinkSerializer(serializers.ModelSerializer):
    """Редактирование/удаление социальных сетей"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SocialLink
        fields = ('name', 'link', 'user')


class CreateSocialLinkSerializer(serializers.ModelSerializer):
    """Добавление социальных сетей"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SocialLink
        fields = ('name', 'link', 'user')

    def create(self, validated_data):
        user = validated_data.pop('user')
        team_id = validated_data.pop('team_id')
        social_link = SocialLink.objects.create(
            team_id=team_id,
            **validated_data
        )
        return social_link


class SocialLinkSerializer(serializers.ModelSerializer):
    """Вывод социальных сетей"""

    class Meta:
        model = SocialLink
        fields = ('name', 'link')


class InvitationSerializer(serializers.ModelSerializer):
    """Сведения о подаче заявок"""
    team = TeamNameView()

    class Meta:
        model = Invitation
        fields = ("id", "team", "user", "create_date", "order_status")


class InvitationAskingSerializer(serializers.ModelSerializer):
    """Подача заявки пользователем"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Invitation
        fields = ("id", "team", "create_date", "user")

    def create(self, validated_data):
        team = validated_data.pop('team')
        cur_user = validated_data.pop('user')
        user = Team.objects.filter(Q(user=cur_user.id) & Q(id=team.id)).exists()
        member = TeamMember.objects.filter(Q(user=cur_user) & Q(team=team)).exists()
        invitation = Invitation.objects.filter(team=team, user=cur_user, order_status='Waiting').exists()
        if user or member or invitation:
            raise CustomException()
        else:
            invitation = Invitation.objects.create(team=team, user=cur_user)
            return invitation


class RetrieveDeleteMember(serializers.ModelSerializer):
    """RD участника команды"""
    user = GetUserSerializer()

    class Meta:
        model = Invitation
        fields = ("id", "create_date", "user")


class AcceptInvitationSerializerList(serializers.ModelSerializer):
    """Вывод заявок для приема в команду"""
    user = GetUserSerializer()
    team = TeamNameView()

    class Meta:
        model = Invitation
        fields = ("id", "team", "create_date", "order_status", "user")


class AcceptInvitationSerializer(serializers.ModelSerializer):
    """Прием в команду"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Invitation
        fields = ("order_status", "user")

    def update(self, instance, validated_data):
        try:
            TeamMember.objects.get(Q(user=instance.user) & Q(team=instance.team))
            raise APIException(
                detail='Участником одной команды можно стать один раз',
                code=status.HTTP_400_BAD_REQUEST
            )
        except TeamMember.DoesNotExist:
            if instance.order_status == 'Approved':
                TeamMember.objects.create(user=instance.user, team=instance.team)
        instance.order_status = validated_data.get('order_status', None)
        instance.save()
        return instance


class TeamMemberSerializer(serializers.ModelSerializer):
    """Просмотр участников команды"""
    user = GetUserSerializer()

    class Meta:
        model = TeamMember
        fields = ("user",)


class ProjectSerializers(serializers.ModelSerializer):
    """Просмотр проекта команды"""

    class Meta:
        model = Project
        fields = ("name",)


class TeamSerializer(serializers.ModelSerializer):
    """Просмотр всех команд"""
    user = GetUserSerializer()
    project_teams = ProjectSerializers(read_only=True, many=True)

    class Meta:
        model = Team
        fields = (
            "id",
            "name",
            "tagline",
            "user",
            "avatar",
            "project_teams"
        )


class TeamListSerializer(serializers.ModelSerializer):
    """Просмотр всех команд как создатель"""
    social_links = SocialLinkSerializer(many=True)

    class Meta:
        model = Team
        fields = ("id", "name", "avatar", "tagline", "social_links")


class CommentChildrenSerializer(serializers.Serializer):
    """ Комментарий к комментарию"""
    def to_representation(self, value):
        serializer = CommentListSerializer(value, context=self.context)
        return serializer.data


class CommentListSerializer(serializers.ModelSerializer):
    """ Список комментариев """
    user = GetUserSerializer()

    class Meta:
        list_serializer_class = FilterCommentListSerializer
        model = Comment
        fields = ("id", "user", "text", "create_date", "comments_count")


class PostSerializer(serializers.ModelSerializer):
    """ Список постов команды """
    user = GetUserSerializer()
    comments = CommentListSerializer(many=True, read_only=True)
    view_count = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "create_date",
            "user",
            "text",
            "view_count",
            "comments",
            "comments_count"
        )


class CreatePost(serializers.ModelSerializer):
    '''Добавление поста'''
    user = GetUserSerializer()

    class Meta:
        model = Post
        fields = ("text", )


class CreateTeamSerializer(serializers.ModelSerializer):
    """Добавить команду"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Team
        fields = (
            "name",
            "tagline",
            "user",
            "avatar",
        )


class UpdateTeamSerializer(serializers.ModelSerializer):
    """Редактирование команды"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Team
        fields = (
            "name",
            "tagline",
            "user",
            "avatar",
        )

    def update(self, instance, validated_data):
        if instance.avatar:
            instance.avatar.delete()
        instance = super().update(instance, validated_data)
        instance.save()
        return instance


class DetailTeamSerializer(serializers.ModelSerializer):
    """ Просмотр деталей одной команды"""
    user = GetUserSerializer()
    social_links = SocialLinkSerializer(many=True)

    class Meta:
        model = Team
        fields = (
            "name",
            "tagline",
            "user",
            "avatar",
            "social_links",
        )


class CommentCreateSerializer(serializers.ModelSerializer):
    """ Добавление комментариев к посту """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ("text", "user", "id", "parent")

    def create(self, validated_data):
        post_id = validated_data.pop('post_id')
        if validated_data.get('parent') is not None:
            try:
                post = Post.objects.get(id=validated_data.get('parent').post.id)
            except Post.DoesNotExist:
                raise APIException(
                    detail='Нет доступа для написания комментариев', code=status.HTTP_400_BAD_REQUEST
                )
            if post.id != post_id:
                raise APIException(
                    detail='Нет доступа для написания комментариев', code=status.HTTP_400_BAD_REQUEST
                )
        comment = Comment.objects.create(
            post_id=post_id,
            **validated_data
            )
        return comment


class TeamCommentUpdateSerializer(serializers.ModelSerializer):
    """ Редактирование/удаление комментариев к посту """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ("text", "user", "id")


class PostCreateSerializer(serializers.ModelSerializer):
    """ CUD поста """

    class Meta:
        model = Post
        fields = ("text", )


class MemberSerializer(serializers.ModelSerializer):
    """Участники команды"""
    user = GetUserSerializer()

    class Meta:
        model = TeamMember
        fields = ("id", "user")


class GetTeamSerializer(serializers.ModelSerializer):
    """Team serializer for other app"""

    class Meta:
        model = Team
        fields = ("id", "name")


