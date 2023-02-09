from rest_framework import serializers

from ..profiles.serializers import GetUserSerializer
from src.repository.models import Project

from . import models
from . import services


class TeamNameView(serializers.ModelSerializer):
    """Сериализатор вывода команды при добавлении социальной ссылки"""

    class Meta:
        model = models.Team
        fields = ('name',)


class ListSocialLinkSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра социальных сетей'"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.SocialLink
        fields = ('id', 'name', 'link', 'user')


class UpdateSocialLinkSerializer(serializers.ModelSerializer):
    """Сериализатор UD социальных сетей"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.SocialLink
        fields = ('name', 'link', 'user')


class CreateSocialLinkSerializer(serializers.ModelSerializer):
    """Сериализатор создания социальных сетей"""
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
    """Сериализатор вывода социальных сетей"""

    class Meta:
        model = models.SocialLink
        fields = ('name', 'link')


class InvitationSerializer(serializers.ModelSerializer):
    """Сериализатор вывода заявок"""
    team = TeamNameView()

    class Meta:
        model = models.Invitation
        fields = ("id", "team", "user", "create_date", "order_status")


class InvitationAskingSerializer(serializers.ModelSerializer):
    """Сериализатор создания заявки пользователем"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Invitation
        fields = ("id", "team", "create_date", "user")

    def create(self, validated_data):
        team = validated_data.pop('team')
        cur_user = validated_data.pop('user')
        return services.check_and_create_invitation(team, cur_user)


class RetrieveDeleteMember(serializers.ModelSerializer):
    """Сериализатор RD участника команды"""
    user = GetUserSerializer()

    class Meta:
        model = models.Invitation
        fields = ("id", "create_date", "user")


class AcceptInvitationSerializerList(serializers.ModelSerializer):
    """Сериализатор вывод заявок для приема в команду"""
    user = GetUserSerializer()
    team = TeamNameView()

    class Meta:
        model = models.Invitation
        fields = ("id", "team", "create_date", "order_status", "user")


class AcceptInvitationSerializer(serializers.ModelSerializer):
    """Сериализатор приема в команду"""
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
    """Сериализатор вывода списка комментариев"""
    user = GetUserSerializer()
    comments_count = serializers.IntegerField()

    class Meta:
        model = models.Comment
        fields = ("id", "user", "text", "create_date", "comments_count")


class CommentCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания комментариев к посту"""
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
    """Сериализатор UD комментариев к посту"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Comment
        fields = ("text", "user", "id")


class CommentChildrenSerializer(serializers.Serializer):
    """Сериализатор вывода комментария к комментарию"""
    def to_representation(self, value):
        serializer = CommentListSerializer(value, context=self.context)
        return serializer.data


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор вывода списока постов команды"""
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
    """Сериализатор CUD поста"""

    class Meta:
        model = models.Post
        fields = ("text",)


class TeamMemberSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра участников команды"""
    user = GetUserSerializer()

    class Meta:
        model = models.TeamMember
        fields = ("user",)


class ProjectSerializers(serializers.ModelSerializer):
    """Сериализатор просмотра проекта команды"""

    class Meta:
        model = Project
        fields = ("name",)


class TeamSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра всех команд"""
    user = GetUserSerializer()
    projects_count = serializers.IntegerField()

    class Meta:
        model = models.Team
        fields = (
            "id",
            "name",
            "tagline",
            "user",
            "avatar",
            "projects_count"
        )


class DetailTeamSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра деталей одной команды"""
    user = GetUserSerializer()
    social_links = SocialLinkSerializer(many=True)
    projects_count = serializers.IntegerField()
    members_count = serializers.IntegerField()

    class Meta:
        model = models.Team
        fields = (
            "name",
            "tagline",
            "user",
            "avatar",
            "social_links",
            "projects_count",
            "members_count"
        )


class CreateTeamSerializer(serializers.ModelSerializer):
    """Сериализатор создания команды"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Team
        fields = (
            "name",
            "tagline",
            "user",
        )


class UpdateTeamSerializer(serializers.ModelSerializer):
    """Сериализатор редактирования команды"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Team
        fields = (
            "name",
            "tagline",
            "user",
        )


class TeamListSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра всех команд как создатель"""
    social_links = SocialLinkSerializer(many=True)

    class Meta:
        model = models.Team
        fields = ("id", "name", "avatar", "tagline", "social_links")


class MemberSerializer(serializers.ModelSerializer):
    """Сериализатор участников команды"""
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
    """Сериализатор аватара команды"""
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


class TeamsSerializer(serializers.ModelSerializer):
    """Сериализатор команд пользователя"""

    class Meta:
        model = models.Team
        fields = ('name',)
