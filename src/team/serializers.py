from django.db.models import Q
from rest_framework import serializers, status
from rest_framework.exceptions import APIException

from ..base.serializers import FilterCommentListSerializer
from .models import Post, Comment, Team, TeamMember, Invitation, SocialLink
from ..profiles.serializers import GetUserSerializer
from ..base.service import delete_old_file


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
            return APIException(
                detail='Добавить ссылку возможно только к своей команде',
                code=status.HTTP_400_BAD_REQUEST
            )


class CreateSocialLinkSerializer(serializers.ModelSerializer):
    """Добавление социальных сетей"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SocialLink
        fields = ('name', 'link', 'user')

    def create(self, validated_data):
        try:
            team = Team.objects.get(
                Q(user=validated_data.get('user').id) &
                Q(id=validated_data.get('team_id'))
            )
        except Team.DoesNotExist:
            raise APIException(
                detail='Добавить ссылку возможно только к своей команде',
                code=status.HTTP_400_BAD_REQUEST
            )
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
        user = Team.objects.filter(
            Q(user=validated_data.get('user').id) & Q(id=validated_data.get('team').id)
        ).exists()
        member = TeamMember.objects.filter(
            Q(user=validated_data.get('user')) & Q(team=validated_data.get('team'))
        ).exists()

        if user or member:
            raise APIException(
                detail='Не возможно стать участником',
                code=status.HTTP_400_BAD_REQUEST
            )
        else:
            invitation = Invitation.objects.create(
                team=validated_data.get('team', None),
                user=validated_data.get('user', None),
            )
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


class TeamSerializer(serializers.ModelSerializer):
    """Просмотр всех команд"""
    user = GetUserSerializer()

    class Meta:
        model = Team
        fields = (
            "id",
            "name",
            "tagline",
            "user",
            "avatar",
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
        try:
            Team.objects.get(Q(user=validated_data.get('user')) & Q(name=instance.name))
        except Team.DoesNotExist:
            raise APIException(
                detail='Нет доступа к данному запросу',
                code=status.HTTP_400_BAD_REQUEST
            )
        instance.name = validated_data.get('name', None)
        instance.tagline = validated_data.get('tagline', None)
        instance.avatar = validated_data.get('avatar', None)
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

#TODO посмотреть метод create как лучше организовать
class CommentCreateSerializer(serializers.ModelSerializer):
    """ Добавление комментариев к посту """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ("text", "user", "id", "parent")

    def create(self, validated_data):
        try:
            post = Post.objects.get(
                Q(team__members__user=validated_data.get('user').id) &
                Q(id=validated_data.get('post_id'))
            )
        except Post.DoesNotExist:
            raise APIException(
                detail='Нет доступа для написания комментариев',
                code=status.HTTP_400_BAD_REQUEST
            )
        if validated_data.get('parent') is not None:
            try:
                post = Post.objects.get(id=validated_data.get('parent').post.id)
            except Post.DoesNotExist:
                raise APIException(
                    detail='Нет доступа для написания комментариев', code=status.HTTP_400_BAD_REQUEST
                )
            if post.id != validated_data.get('post_id'):
                raise APIException(
                    detail='Нет доступа для написания комментариев', code=status.HTTP_400_BAD_REQUEST
                )
            comment = Comment.objects.create(
                text=validated_data.get('text', None),
                user=validated_data.get('user', None),
                post=post,
                parent=validated_data.get('parent', None)
                )
            return comment
        else:
            comment = Comment.objects.create(
                text=validated_data.get('text', None),
                user=validated_data.get('user', None),
                post=post,
                parent=validated_data.get('parent', None)
            )
            return comment


class TeamCommentUpdateSerializer(serializers.ModelSerializer):
    """ Редактирование/удаление комментариев к посту """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ("text", "user", "id")

    def update(self, instance, validated_data):
        try:
            Comment.objects.get(Q(user=validated_data.get('user')) & Q(id=validated_data.get('id')))
        except Comment.DoesNotExist:
            raise APIException(
                detail='Нет доступа к данному запросу',
                code=status.HTTP_400_BAD_REQUEST
            )
        instance.text = validated_data.get('text', None)
        instance.save()
        return instance


class PostUpdateSerializer(serializers.ModelSerializer):
    """ CUD поста """

    class Meta:
        model = Post
        fields = ("text", )

    def create(self, validated_data):
        try:
            team = Team.objects.get(Q(user=validated_data.get('user')) & Q(id=validated_data.get('team_id')))
        except:
            raise APIException(
                detail='Нет доступа для создания поста', code=status.HTTP_400_BAD_REQUEST
            )
        post = Post.objects.create(
            text=validated_data.get('text', None),
            user=validated_data.get('user', None),
            team=team,
        )
        return post

    def update(self, instance, validated_data):
        try:
            Post.objects.get(Q(user=validated_data.get('user')) & Q(id=validated_data.get('id')))
        except Post.DoesNotExist:
            raise APIException(
                detail='Нет доступа к данному запросу',
                code=status.HTTP_400_BAD_REQUEST
            )
        instance.text = validated_data.get('text', None)
        instance.save()
        return instance


class TeamUpdateSerializer(serializers.ModelSerializer):
    """ Редактирование поста """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ("id", "user", "create_date", "text")

    def update(self, instance, validated_data):
        try:
            member = Team.objects.get(Q(user=instance.user) & Q(name=instance.team))
        except TeamMember.DoesNotExist:
            return APIException(
                detail='Участником одной команды можно стать один раз',
                code=status.HTTP_400_BAD_REQUEST
            )
        instance.text = validated_data.get('text', None)
        instance.save()
        return instance


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


