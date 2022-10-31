from django.db.models import Q
from rest_framework import serializers, status
from rest_framework.exceptions import APIException

from ..base.serializers import FilterCommentListSerializer
from .models import Post, Comment, Team, TeamMember, Invitation, SocialLink
from ..profiles.serializers import GetUserSerializer
from ..base.service import delete_old_file


class TeamSocialLinkView(serializers.ModelSerializer):
    """Вывод команды при добавлении социальной ссылки"""

    class Meta:
        model = Team
        fields = ('name',)


class ListSocialLinkSerializer(serializers.ModelSerializer):
    """Просмотр социальных сетей"""
    team = TeamSocialLinkView()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SocialLink
        fields = ('id', 'name', 'link', 'team', 'user')


class UpdateSocialLinkSerializer(serializers.ModelSerializer):
    """Редактирование/удаление социальных сетей"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SocialLink
        fields = ('name', 'link', 'user')

    def update(self, instance, validated_data):
        try:
            team = Team.objects.get(
                Q(user=validated_data.get('user').id) & Q(name=instance.team)
            )
            instance.name = validated_data.get('name', None)
            instance.link = validated_data.get('link', None)
            instance.team = team
            instance.save()
            return instance
        except Team.DoesNotExist:
            raise APIException(
                detail='Добавить ссылку возможно только к своей команде',
                code=status.HTTP_400_BAD_REQUEST
            )


class CreateSocialLinkSerializer(serializers.ModelSerializer):
    """Добавление социальных сетей"""
    team = TeamSocialLinkView()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SocialLink
        fields = ('name', 'link', 'team', 'user')

    def create(self, validated_data):
        try:
            team = Team.objects.get(
                Q(user=validated_data.get('user').id) &
                Q(name=validated_data.get('team').get('name'))
            )
        except Team.DoesNotExist:
            raise APIException(
                detail='Добавить ссылку возможно только к своей команде',
                code=status.HTTP_400_BAD_REQUEST
            )
        try:
            social_link = SocialLink.objects.get(team__name=validated_data.get('team').get('name'))
            raise APIException(
                detail='Добавить ссылку к команде только одну',
                code=status.HTTP_400_BAD_REQUEST
            )
        except SocialLink.DoesNotExist:
            social_link = SocialLink.objects.create(
                name=validated_data.get('name', None),
                link=validated_data.get('link', None),
                team=team
            )
            return social_link


class SocialLinkSerializer(serializers.ModelSerializer):
    """Вывод социальных сетей"""

    class Meta:
        model = SocialLink
        fields = ('name', 'link')

# Как изменить что бы показывал статус а не цифру?
class InvitationSerializer(serializers.ModelSerializer):
    """Сведения о подаче заявок"""
    team = TeamSocialLinkView()

    class Meta:
        model = Invitation
        fields = ("id", "team", "user", "create_date", "order_status")

# как в try два запроса проверить?
class InvitationAskingSerializer(serializers.ModelSerializer):
    """Подача заявки пользователем"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Invitation
        fields = ("id", "team", "create_date", "user")

    def create(self, validated_data):
        user = Team.objects.filter(
            Q(user=validated_data.get('user').id) & Q(id=validated_data.get('team').id)
        ).exists()
        member = TeamMember.objects.filter(
            Q(user=validated_data.get('user')) & Q(team=validated_data.get('team'))
        ).exists()

        if user or member:
            raise APIException(
                detail='Не возможно стать участником своей команды',
                code=status.HTTP_400_BAD_REQUEST
            )
        else:
            invitation = Invitation.objects.create(
                team=validated_data.get('team', None),
                user=validated_data.get('user', None),
            )
            return invitation


class AcceptInvitationSerializerList(serializers.ModelSerializer):
    """Вывод заявок для приема в команду"""
    user = GetUserSerializer()
    team = TeamSocialLinkView()

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


class TeamSerializer(serializers.ModelSerializer):
    """Просмотр всех команд"""
    user = GetUserSerializer()

    class Meta:
        model = Team
        fields = ("name", "tagline", "user", "avatar")


class TeamListSerializer(serializers.ModelSerializer):
    """Просмотр всех команд как создатель"""
    members = TeamMemberSerializer(many=True, read_only=True)
    social_links = SocialLinkSerializer(many=True)

    class Meta:
        model = Team
        fields = ("id", "name", "avatar", "tagline", "members", "social_links")


class TeamCommentChildrenListSerializer(serializers.ModelSerializer):
    """ Комментарий к комментарию"""
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
    """Добавление поста"""
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


class TeamMemberRetrieveSerializer(serializers.ModelSerializer):
    """Просмотр одной команд как участник"""
    members = TeamMemberSerializer(many=True, read_only=True)
    articles = TeamListPostSerializer(many=True)
    social_links = SocialLinkSerializer(many=True)
    team = TeamSerializer(many=True)

    class Meta:
        model = Team
        fields = ("id", "name", "avatar", "tagline", "articles", "members", "social_links")


class CreateTeamSerializer(serializers.ModelSerializer):
    """Добавить команду"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Team
        fields = ("name", "tagline", "user", "avatar")

# TODO два одинаковых сериализатора
class UpdateTeamSerializer(serializers.ModelSerializer):
    """Редактирование команды"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Team
        fields = ("name", "tagline", "user", "avatar")


class DetailTeamSerializer(serializers.ModelSerializer):
    """ Просмотр деталей одной команды"""
    user = GetUserSerializer()
    social_links = SocialLinkSerializer(many=True)

    class Meta:
        model = Team
        fields = ("name", "tagline", "user", "avatar", "social_links")


class TeamCommentCreateSerializer(serializers.ModelSerializer):
    """ Добавление комментариев к посту """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ("text", "post", "user")

    def create(self, validated_data):
        try:
            post = Post.objects.get(
                Q(team__members__user=validated_data.get('user').id) &
                Q(id=validated_data.get('post').id)
            )
        except Post.DoesNotExist:
            raise APIException(
                detail='Нет доступа для написания комментариев', code=status.HTTP_400_BAD_REQUEST
            )
        comment = Comment.objects.create(
            text=validated_data.get('text', None),
            user=validated_data.get('user', None),
            post=validated_data.get('post', None),
        )
        return comment


class TeamPostSerializer(serializers.ModelSerializer):
    """ Вывод и создание поста """
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




# class TeamSerializerforMember(serializers.ModelSerializer):
#     """ Team serializer for member """
#
#     class Meta:
#         model = Team
#         fields = "__all__"
#
#
# class TeamAvatarSerializer(serializers.ModelSerializer):
#     """ Team avatar serializer """
#
#     class Meta:
#         model = Team
#         fields = ("avatar",)
#
#     def update(self, instance, validated_data):
#         if instance.avatar:
#             delete_old_file(instance.avatar.path)
#         return super().update(instance, validated_data)


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

#
# class AllTeamSerializers(serializers.ModelSerializer):
#     '''Команды'''
#     user = GetUserSerializer()
#
#     class Meta:
#         model = Team
#         fields = '__all__'
#
#
# class AllMembersTeamSerializers(serializers.ModelSerializer):
#     '''Команды'''
#     user = GetUserSerializer()
#
#     class Meta:
#         model = Team
#         fields = '__all__'
#
#
# class ByUserTeamMemberSerializer(serializers.ModelSerializer):
#     """TeamMember serializer"""
#     team = AllTeamSerializers(read_only=True)
#     members = TeamMemberSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = TeamMember
#         fields = ("team", "members")
#
#
# class ByUserTeamListSerializer(serializers.ModelSerializer):
#     """By user Team list serializer"""
#     members = ByUserTeamMemberSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Team
#         fields = ("id", "name", "avatar", "tagline", "members")


class GetTeamSerializer(serializers.ModelSerializer):
    """Team serializer for other app"""

    class Meta:
        model = Team
        fields = ("id", "name")


