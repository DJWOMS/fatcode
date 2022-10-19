from rest_framework import serializers

from ..base.serializers import FilterCommentListSerializer
from .models import Post, Comment, Team, TeamMember, Invitation, SocialLink
from ..profiles.serializers import GetUserSerializer
from ..base.service import delete_old_file


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = '__all__'


# class InvitationListSerializer(serializers.ModelSerializer):
#     """Invitation list serializer"""
#     user = GetUserSerializer()
#     team = serializers.ReadOnlyField(source='team.name')
#
#     class Meta:
#         model = Invitation
#         fields = ("id", "team", "user", "asking", "create_date")
#
#
# class InvitationSerializer(serializers.ModelSerializer):
#     """Invitation detail serializer"""
#
#     class Meta:
#         model = Invitation
#         fields = ("id", "team", "user", "create_date")
#
#
# class InvitationAskingSerializer(serializers.ModelSerializer):
#     """Invitation detail serializer"""
#
#     class Meta:
#         model = Invitation
#         fields = ("id", "team", "create_date")


class AcceptInvitationSerializer(serializers.ModelSerializer):
    """Accepted invitation serializer"""

    class Meta:
        model = Invitation
        fields = ("accepted",)


class TeamMemberSerializer(serializers.ModelSerializer):
    """TeamMember serializer"""
    user = GetUserSerializer()

    class Meta:
        model = TeamMember
        fields = ("team", "user",)


class TeamSerializer(serializers.ModelSerializer):
    """Просмотр всех команд"""
    user = GetUserSerializer()

    class Meta:
        model = Team
        fields = (
            "name",
            "tagline",
            "user",
            "avatar",
        )


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


# как сделать не обязательное поле social_links?
class UpdateTeamSerializer(serializers.ModelSerializer):
    """Редактирование команды"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    social_links = SocialLinkSerializer(many=True)

    class Meta:
        model = Team
        fields = (
            "name",
            "tagline",
            "user",
            "avatar",
            "social_links"
        )

    def update(self, instanse, validated_data):
        print(instanse)
        print(validated_data)
        instanse.name = validated_data.get('name', None)
        instanse.tagline = validated_data.get('tagline', None)
        instanse.avatar = validated_data.get('avatar', None)
        instanse.user = validated_data.get('user', None)
        team = SocialLink.objects.get(name=instanse.name)
        if validated_data.get('social_links'):
            social_links, _ = SocialLink.update_or_create(
                team=team,
                defaults={'name': validated_data.get('name', None),
                          'links': validated_data.get('links', None)}

            )
            return social_links


class TeamCommentChildrenListSerializer(serializers.ModelSerializer):
    """ Comment children list serializer"""
    user = GetUserSerializer()

    class Meta:
        model = Comment
        fields = ("id", "user", "text", "create_date")


class TeamCommentListSerializer(serializers.ModelSerializer):
    """ Список комментариев """
    user = GetUserSerializer()
    children = TeamCommentChildrenListSerializer(read_only=True, many=True)

    class Meta:
        list_serializer_class = FilterCommentListSerializer
        model = Comment
        fields = ("id", "user", "text", "create_date", "children")

# Got AttributeError when attempting to get a value for field `comments` on serializer `DetailTeamSerializer`.
# The serializer field might be named incorrectly and not match any attribute or key on the `Team` instance.
# Original exception text was: 'Team' object has no attribute 'comments'. Но комментариев нет в данном сериализаторе DetailTeamSerializer
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


class TeamCommentCreateSerializer(serializers.ModelSerializer):
    """ Добавление комментариев к посту """

    class Meta:
        model = Comment
        fields = ("post", "text", "parent")


class TeamPostSerializer(serializers.ModelSerializer):
    """ Вывод и редактирование поста """
    user = GetUserSerializer(read_only=True)
    comments = TeamCommentListSerializer(many=True, read_only=True)
    view_count = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = ("id", "team", "user", "create_date", "text", "comments", "view_count")


class TeamListPostSerializer(serializers.ModelSerializer):
    """ Список постов """
    user = GetUserSerializer()
    comments = TeamCommentListSerializer(many=True, read_only=True)
    view_count = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "team",
            "create_date",
            "user",
            "text",
            "view_count",
            "comments",
            "comments_count"
        )


class TeamSerializerforMember(serializers.ModelSerializer):
    """ Team serializer for member """

    class Meta:
        model = Team
        fields = "__all__"


class TeamAvatarSerializer(serializers.ModelSerializer):
    """ Team avatar serializer """

    class Meta:
        model = Team
        fields = ("avatar",)

    def update(self, instance, validated_data):
        if instance.avatar:
            delete_old_file(instance.avatar.path)
        return super().update(instance, validated_data)


class TeamListSerializer(serializers.ModelSerializer):
    """Просмотр всех команд как создатель"""
    members = TeamMemberSerializer(many=True, read_only=True)
    social_links = SocialLinkSerializer(many=True)
    class Meta:
        model = Team
        fields = ("id", "name", "avatar", "tagline", "members", "social_links")
#Почему не выводяться посты?
class TeamRetrieveSerializer(serializers.ModelSerializer):
    """Просмотр одной команд как создатель"""
    members = TeamMemberSerializer(many=True, read_only=True)
    posts = TeamListPostSerializer(many=True)

    class Meta:
        model = Team
        fields = ("id", "name", "avatar", "tagline", "members", "posts")


class AllTeamSerializers(serializers.ModelSerializer):
    '''Команды'''
    user = GetUserSerializer()

    class Meta:
        model = Team
        fields = '__all__'


class AllMembersTeamSerializers(serializers.ModelSerializer):
    '''Команды'''
    user = GetUserSerializer()

    class Meta:
        model = Team
        fields = '__all__'


# Почему не показывает memebers?
class ByUserTeamMemberSerializer(serializers.ModelSerializer):
    """TeamMember serializer"""
    team = AllTeamSerializers(read_only=True)
    members = TeamMemberSerializer(many=True, read_only=True)

    class Meta:
        model = TeamMember
        fields = ("team", "members")


class ByUserTeamListSerializer(serializers.ModelSerializer):
    """By user Team list serializer"""
    members = ByUserTeamMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ("id", "name", "avatar", "tagline", "members")


class GetTeamSerializer(serializers.ModelSerializer):
    """Team serializer for other app"""

    class Meta:
        model = Team
        fields = ("id", "name")


class DetailTeamSerializer(serializers.ModelSerializer):
    """ Просмотр деталей одной команды"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    social_links = SocialLinkSerializer(many=True)
    comments = TeamCommentListSerializer(many=True)

    class Meta:
        model = Team
        fields = (
            "name",
            "tagline",
            "user",
            "avatar",
            "social_links",
            "comments"
        )
