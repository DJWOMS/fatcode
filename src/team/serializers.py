from rest_framework import serializers

from ..base.serializers import FilterCommentListSerializer
from .models import Post, Comment, Team, TeamMember, Invitation, SocialLink
from ..profiles.serializers import GetUserSerializer
from ..base.service import delete_old_file


class SocialLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = SocialLink
        fields = ('name', 'link')


class InvitationListSerializer(serializers.ModelSerializer):
    """Invitation list serializer"""
    user = GetUserSerializer()
    team = serializers.ReadOnlyField(source='team.name')

    class Meta:
        model = Invitation
        fields = ("id", "team", "user", "asking", "create_date")


class InvitationSerializer(serializers.ModelSerializer):
    """Сведения о подаче заявок"""

    class Meta:
        model = Invitation
        fields = ("id", "team", "user", "create_date")


class InvitationAskingSerializer(serializers.ModelSerializer):
    """Подача заявки пользователем"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Invitation
        fields = ("id", "team", "create_date", "user")


# class AcceptInvitationSerializer(serializers.ModelSerializer):
#     """Accepted invitation serializer"""
#
#     class Meta:
#         model = Invitation
#         fields = ("accepted",)


class TeamMemberSerializer(serializers.ModelSerializer):
    """Просмотр участников команды"""
    user = GetUserSerializer()

    class Meta:
        model = TeamMember
        fields = ("user",)

class TeamListSerializer(serializers.ModelSerializer):
    """Просмотр всех команд как создатель"""
    members = TeamMemberSerializer(many=True, read_only=True)
    social_links = SocialLinkSerializer(many=True)
    class Meta:
        model = Team
        fields = ("id", "name", "avatar", "tagline", "members", "social_links")


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
class CreatePost(serializers.ModelSerializer):
    '''Добавление поста'''
    user = GetUserSerializer()

    class Meta:
        model = Post
        fields = ("text", )


class TeamRetrieveSerializer(serializers.ModelSerializer):
    """Просмотр одной команд как создатель"""
    members = TeamMemberSerializer(many=True, read_only=True)
    articles = TeamListPostSerializer(many=True)
    social_links = SocialLinkSerializer(many=True)

    class Meta:
        model = Team
        fields = ("id", "name", "avatar", "tagline", "articles", "members", "social_links")

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
# и что нужно вернуть в update?
class UpdateTeamSerializer(serializers.ModelSerializer):
    """Редактирование команды"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    social_links = SocialLinkSerializer()

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
        social_links_data = validated_data.get('social_links')
        instanse.name = validated_data.get('name', None)
        instanse.tagline = validated_data.get('tagline', None)
        instanse.avatar = validated_data.get('avatar', None)
        instanse.user = validated_data.get('user', None)
        try:
            social_link = SocialLink.objects.get(team=instanse)
            social_link.team = instanse
            social_link.name = social_links_data.get('name')
            social_link.link = social_links_data.get('link')
            return social_link
        except SocialLink.DoesNotExist:
            social_link = SocialLink.objects.create(team=instanse,
                                      name=social_links_data.get('name'),
                                      link=social_links_data.get('link'))
            return social_link



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
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    comments = TeamCommentListSerializer(many=True, read_only=True)
    view_count = serializers.CharField(read_only=True)

    class Meta:
        model = Post
        fields = ("id", "user", "create_date", "text", "comments", "view_count", "team")

    def create(self, validated_data):
        post = Post.objects.create(
            text=validated_data.get('text', None),
            user=validated_data.get('user', None),
            team=validated_data.get('team', None),
        )
        return post




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


# class TeamListSerializer(serializers.ModelSerializer):
#     """Просмотр всех команд как создатель"""
#     members = TeamMemberSerializer(many=True, read_only=True)
#     social_links = SocialLinkSerializer(many=True)
#     class Meta:
#         model = Team
#         fields = ("id", "name", "avatar", "tagline", "members", "social_links")
# #Почему не выводяться посты?
# class TeamRetrieveSerializer(serializers.ModelSerializer):
#     """Просмотр одной команд как создатель"""
#     members = TeamMemberSerializer(many=True, read_only=True)
#     # posts = TeamListPostSerializer(many=True)
#     social_links = SocialLinkSerializer(many=True)
#
#     class Meta:
#         model = Team
#         fields = ("id", "name", "avatar", "tagline", "members", "social_links")


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


