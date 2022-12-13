from rest_framework import serializers

from ..profiles.serializers import GetUserSerializer
from src.repository.models import Project

from . import models
from . import services


class TeamNameView(serializers.ModelSerializer):
    """Вывод команды при добавлении социальной ссылки"""

    class Meta:
        model = models.Team
        fields = ('name',)


class ListSocialLinkSerializer(serializers.ModelSerializer):
    """Просмотр социальных сетей'"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.SocialLink
        fields = ('id', 'name', 'link', 'user')


class UpdateSocialLinkSerializer(serializers.ModelSerializer):
    """Редактирование/удаление социальных сетей"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.SocialLink
        fields = ('name', 'link', 'user')


class CreateSocialLinkSerializer(serializers.ModelSerializer):
    """Добавление социальных сетей"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.SocialLink
        fields = ('name', 'link', 'user')

    def create(self, validated_data):
        user = validated_data.pop('user')
        team_id = validated_data.pop('team_id')
        social_link = models.SocialLink.objects.create(
            team_id=team_id,
            **validated_data
        )
        return social_link


class SocialLinkSerializer(serializers.ModelSerializer):
    """Вывод социальных сетей"""

    class Meta:
        model = models.SocialLink
        fields = ('name', 'link')


class InvitationSerializer(serializers.ModelSerializer):
    """Сведения о подаче заявок"""
    team = TeamNameView()

    class Meta:
        model = models.Invitation
        fields = ("id", "team", "user", "create_date", "order_status")


class InvitationAskingSerializer(serializers.ModelSerializer):
    """Подача заявки пользователем"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Invitation
        fields = ("id", "team", "create_date", "user")

    def create(self, validated_data):
        team = validated_data.pop('team')
        cur_user = validated_data.pop('user')
        return services.check_and_create_invitation(team, cur_user)


class RetrieveDeleteMember(serializers.ModelSerializer):
    """RD участника команды"""
    user = GetUserSerializer()

    class Meta:
        model = models.Invitation
        fields = ("id", "create_date", "user")


class AcceptInvitationSerializerList(serializers.ModelSerializer):
    """Вывод заявок для приема в команду"""
    user = GetUserSerializer()
    team = TeamNameView()

    class Meta:
        model = models.Invitation
        fields = ("id", "team", "create_date", "order_status", "user")


class AcceptInvitationSerializer(serializers.ModelSerializer):
    """Прием в команду"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Invitation
        fields = ("order_status", "user")

    def update(self, instance, validated_data):
        services.check_and_create_team_member(instance)
        instance.order_status = validated_data.get('order_status', None)
        instance.save()
        return instance


class CommentListSerializer(serializers.ModelSerializer):
    """ Список комментариев """
    user = GetUserSerializer()
    comments_count = serializers.IntegerField()

    class Meta:
        model = models.Comment
        fields = ("id", "user", "text", "create_date", "comments_count")


class CommentCreateSerializer(serializers.ModelSerializer):
    """ Добавление комментариев к посту """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Comment
        fields = ("text", "user", "id", "parent")

    def create(self, validated_data):
        post_id = validated_data.pop('post_id')
        services.check_post(post_id, **validated_data)
        comment = models.Comment.objects.create(
            post_id=post_id,
            **validated_data
            )
        return comment


class TeamCommentUpdateSerializer(serializers.ModelSerializer):
    """ Редактирование/удаление комментариев к посту """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Comment
        fields = ("text", "user", "id")


class CommentChildrenSerializer(serializers.Serializer):
    """ Комментарий к комментарию"""
    def to_representation(self, value):
        serializer = CommentListSerializer(value, context=self.context)
        return serializer.data


class PostSerializer(serializers.ModelSerializer):
    """ Список постов команды """
    user = GetUserSerializer()
    view_count = serializers.CharField(read_only=True)
    comments_count = serializers.IntegerField()

    class Meta:
        model = models.Post
        fields = (
            "id",
            "create_date",
            "user",
            "text",
            "view_count",
            "comments_count"
        )


class PostCreateSerializer(serializers.ModelSerializer):
    """ CUD поста """

    class Meta:
        model = models.Post
        fields = ("text",)


class TeamMemberSerializer(serializers.ModelSerializer):
    """Просмотр участников команды"""
    user = GetUserSerializer()

    class Meta:
        model = models.TeamMember
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
        model = models.Team
        fields = (
            "id",
            "name",
            "tagline",
            "user",
            "avatar",
            "project_teams"
        )


class DetailTeamSerializer(serializers.ModelSerializer):
    """ Просмотр деталей одной команды"""
    user = GetUserSerializer()
    social_links = SocialLinkSerializer(many=True)

    class Meta:
        model = models.Team
        fields = (
            "name",
            "tagline",
            "user",
            "avatar",
            "social_links",
        )


class CreateTeamSerializer(serializers.ModelSerializer):
    """Добавить команду"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Team
        fields = (
            "name",
            "tagline",
            "user",
        )


class UpdateTeamSerializer(serializers.ModelSerializer):
    """Редактирование команды"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Team
        fields = (
            "name",
            "tagline",
            "user",
        )


class TeamListSerializer(serializers.ModelSerializer):
    """Просмотр всех команд как создатель"""
    social_links = SocialLinkSerializer(many=True)

    class Meta:
        model = models.Team
        fields = ("id", "name", "avatar", "tagline", "social_links")


class MemberSerializer(serializers.ModelSerializer):
    """Участники команды"""
    user = GetUserSerializer()

    class Meta:
        model = models.TeamMember
        fields = ("id", "user")


class GetTeamSerializer(serializers.ModelSerializer):
    """Team serializer for other app"""

    class Meta:
        model = models.Team
        fields = ("id", "name")


class AvatarSerializer(serializers.ModelSerializer):
    """ Аватар команды """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Team
        fields = ('avatar', 'user')

    def update(self, instance, validated_data):
        if instance.avatar:
            instance.avatar.delete()
        instance = super().update(instance, validated_data)
        instance.save()
        return instance
