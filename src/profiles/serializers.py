import os

from djoser.serializers import UserSerializer, UserCreatePasswordRetypeSerializer
from djoser.conf import settings
from rest_framework import serializers

# from src.courses.serializers import ListCourseSerializer
from src.profiles import models, services
from src.repository.models import Toolkit
from src.profiles import models
from src.base.validators import ImageValidator
from src.profiles.services import add_friend
from src.base import exceptions


class UserUpdateSerializer(UserSerializer):
    """Serialization to change user data"""

    class Meta:
        model = models.FatUser
        fields = tuple(models.FatUser.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'first_name',
            'last_name',
            'middle_name'
        )
        read_only_fields = (settings.LOGIN_FIELD,)


class UsersCreateSerializer(UserCreatePasswordRetypeSerializer):
    """Serialization to create user data"""
    email = serializers.EmailField(required=True)
    invite = serializers.CharField(max_length=50)

    class Meta:
        model = models.FatUser
        fields = ('username', 'email', 'password', 'invite')

    def validate(self, attrs):
        self.fields.pop("invite", None)
        invite = attrs.pop('invite')
        services.check_email(attrs.get('email'))
        services.check_invite(invite)
        attrs = super().validate(attrs)
        if attrs:
            services.delete_invite(invite)
            return attrs
        raise exceptions.AuthExists()


class UserSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FatUserSocial
        fields = '__all__'


class ListSocialSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(read_only=True)

    class Meta:
        model = models.Social
        fields = '__all__'


class UserAvatarSerializer(serializers.ModelSerializer):
    """Update user avatar"""
    avatar = serializers.ImageField(validators=[ImageValidator((100, 100), 1048576)])

    class Meta:
        model = models.FatUser
        fields = [
            "id",
            "avatar"
        ]


class AccountSerializer(serializers.ModelSerializer):
    """Serialization for user's git_hub account"""

    class Meta:
        model = models.Account
        fields = ("account_url", )


class UserSerializer(serializers.ModelSerializer):
    """Serialization for user's internal display"""
    email = serializers.EmailField(read_only=True)
    avatar = serializers.ImageField(validators=[ImageValidator((100, 100), 1048576)])
    user_social = UserSocialSerializer(many=True)
    socials = ListSocialSerializer(many=True)
    # courses = serializers.ListCourseSerializer(many=True)
    user_account = AccountSerializer(read_only=True, many=True)

    class Meta:
        model = models.FatUser
        exclude = (
            "password",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions"
        )
        ref_name = "Fat user"

    def update(self, instance, validated_data):
        if validated_data.get('user_social', None):
            user_social = validated_data.pop('user_social')
            self.update_user_social(instance, user_social)

        return super().update(instance, validated_data)

    def update_user_social(self, instance, user_social):
        for soc in user_social:
            entry_fatUserSocial = instance.user_social.filter(
                social=soc['social']).first()

            if entry_fatUserSocial is not None:
                entry_fatUserSocial.user_url = soc['user_url']
                entry_fatUserSocial.save()
            else:
                instance.user_social.create(social=soc['social'], user_url=soc['user_url'])


class UserPublicSerializer(serializers.ModelSerializer):
    """Serialization for public user display"""

    avatar = serializers.ImageField(read_only=True)
    user_social = UserSocialSerializer(many=True)
    socials = ListSocialSerializer(many=True)
    # courses = ListCourseSerializer(many=True)

    class Meta:
        model = models.FatUser
        exclude = (
            "email",
            "password",
            "last_login",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )


class GetUserSerializer(serializers.ModelSerializer):
    """Serialization for other serializers"""

    class Meta:
        model = models.FatUser
        fields = ("id", "username", "avatar")


class GetUserForProjectSerializer(serializers.ModelSerializer):
    """Serialization for other serializers"""

    class Meta:
        model = models.FatUser
        fields = ("id", "username")


class DashboardUserSerializer(serializers.ModelSerializer):
    """Serializer for dashboard"""
    started_courses_count = serializers.SerializerMethodField()
    finished_courses_count = serializers.SerializerMethodField()

    class Meta:
        model = models.FatUser
        fields = (
                'coins',
                'experience',
                'username',
                'id',
                'started_courses_count',
                'finished_courses_count'
            )

        def get_started_courses_count(self, instance):
            return instance.courses.filter(progress=0).count()

        def get_finished_courses_count(self, instance):
            return instance.courses.filter(progress=100).count()


class GitHubAddSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=25)


class QuestionnaireSerializer(serializers.ModelSerializer):
    """ Анкета пользователя """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Questionnaire
        fields = (
            "description",
            "country",
            "town",
            "phone",
            "user",
            "toolkits",
            "teams",
            "projects",
            "accounts",
            "socials",
            "languages"
        )

    def create(self, validated_data):
        teams = validated_data.pop('teams', None)
        toolkits = validated_data.pop('toolkits', None)
        projects = validated_data.pop('projects', None)
        accounts = validated_data.pop('accounts', None)
        user = validated_data.pop('user')
        languages = validated_data.pop('languages', None)
        socials = validated_data.pop('socials', None)
        services.check_profile(user, teams, projects, accounts, socials)
        return services.questionnaire_create(
            user,
            teams,
            projects,
            accounts,
            toolkits,
            languages,
            socials,
            **validated_data
        )

    def update(self, instance, validated_data):
        teams = validated_data.pop('teams', None)
        toolkits = validated_data.pop('toolkits', None)
        projects = validated_data.pop('projects', None)
        accounts = validated_data.pop('accounts', None)
        user = validated_data.pop('user')
        languages = validated_data.pop('languages', None)
        socials = validated_data.pop('socials', None)
        services.check_profile(user, teams, projects, accounts, socials)
        instance = super().update(instance, validated_data)
        instance = services.questionnaire_update(instance, teams, toolkits, projects, accounts, languages, socials)
        instance.save()
        return instance


class GetToolkitForUserSerializer(serializers.ModelSerializer):
    """Инструментарий"""

    class Meta:
        model = Toolkit
        fields = ('name', )


class QuestionnaireListSerializer(serializers.ModelSerializer):
    """Список анкет"""
    user = GetUserSerializer()
    toolkits = GetToolkitForUserSerializer(many=True)

    class Meta:
        model = models.Questionnaire
        fields = ('id', 'user', 'toolkits')


class TokenSerializer(serializers.Serializer):
    """Сериализатор Токена"""
    auth_token = serializers.CharField(max_length=255)


class ApplicationListSerializer(serializers.ModelSerializer):
    getter = GetUserSerializer()

    class Meta:
        model = models.Applications
        fields = ('id', 'getter', )


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Applications
        fields = ('id', 'getter', )


class FriendListSerializer(serializers.ModelSerializer):
    friend = GetUserSerializer()

    class Meta:
        model = models.Friends
        fields = ('id', 'friend', )

    def create(self, validated_data):
        return add_friend(friend=validated_data['friend'], user=validated_data['user'])


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Friends
        fields = ('id', 'friend', )

    def create(self, validated_data):
        return add_friend(friend=validated_data['friend'], user=validated_data['user'])


class AvatarProfileSerializer(serializers.ModelSerializer):
    """ Аватар профиля """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.FatUser
        fields = ('avatar', 'user')

    def update(self, instance, validated_data):
        if instance.avatar:
            instance.avatar.delete()
        instance.avatar = validated_data.get('avatar', None)
        instance.save()
        return instance


class AvatarQuestionnaireSerializer(serializers.ModelSerializer):
    """ Аватар анкеты """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Questionnaire
        fields = ('avatar', 'user')

    def update(self, instance, validated_data):
        if instance.avatar:
            instance.avatar.delete()
        instance.avatar = validated_data.get('avatar', None)
        instance.save()
        return instance


class SocialSerializer(serializers.ModelSerializer):
    """Социальные ссылки"""

    class Meta:
        model = models.Social
        fields = ('title', )


class SocialProfileSerializer(serializers.ModelSerializer):
    """ Просмотр социальных ссылок профиля """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    social = SocialSerializer()

    class Meta:
        model = models.FatUserSocial
        fields = ('id', 'social', 'user', 'user_url')


class SocialProfileCreateSerializer(serializers.ModelSerializer):
    """ Create социальных ссылок профиля """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.FatUserSocial
        fields = ('id', 'social', 'user', 'user_url')

    def create(self, validated_data):
        user = validated_data.pop('user')
        social_link = validated_data.pop('social')
        user_url = validated_data.pop('user_url')
        cur_social = models.FatUserSocial.objects.filter(social=social_link, user=user).exists()
        if cur_social:
            raise exceptions.SocialExists()
        social = models.FatUserSocial.objects.create(social=social_link, user=user, user_url=user_url)
        return social


class SocialProfileUpdateSerializer(serializers.ModelSerializer):
    """ Update социальных ссылок профиля """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.FatUserSocial
        fields = ('id', 'user', 'user_url')


class UserProfileSerializer(serializers.ModelSerializer):
    """ Представление профиля """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.FatUser
        fields = ('id', 'avatar', 'middle_name', 'email', 'user')


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """ RUDE профиля """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.FatUser
        fields = ('id', 'middle_name', 'email', 'user')

    def update(self, instance, validated_data):
        email = validated_data.pop('email')
        return services.check_or_update_email(instance, email, validated_data)


class SocialListSerializer(serializers.ModelSerializer):
    """Просмотр социальных сетей"""

    class Meta:
        model = models.Social
        fields = ('title', 'logo', 'url')

