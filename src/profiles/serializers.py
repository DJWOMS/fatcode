from djoser.serializers import UserSerializer, UserCreatePasswordRetypeSerializer
from djoser.conf import settings

from rest_framework import serializers
from src.courses.serializers import ListCourseSerializer
from src.profiles import models, services
from src.base.validators import ImageValidator
from src.repository.models import Toolkit
from ..base import exceptions
from .models import FatUser

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

    class Meta:
        model = models.FatUser
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        email = validated_data.pop('email', None)
        password = validated_data.pop('password', None)
        return services.check_and_create_user(email, password, **validated_data)


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
    courses = ListCourseSerializer(many=True)
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
    courses = ListCourseSerializer(many=True)

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
            "avatar",
            "user",
            "toolkit",
            "teams",
            "projects",
            "accounts",
            "socials",
            "category"
        )

    def create(self, validated_data):
        teams = validated_data.pop('teams', None)
        toolkit = validated_data.pop('toolkit', None)
        projects = validated_data.pop('projects', None)
        accounts = validated_data.pop('accounts', None)
        user = validated_data.pop('user')
        languages = validated_data.pop('category', None)
        socials = validated_data.pop('socials', None)
        check_profile = services.check_profile(user, teams, projects, accounts, socials)
        questionnaire = services.questionnaire_create(user,
                                                      teams,
                                                      projects,
                                                      accounts,
                                                      toolkit,
                                                      languages,
                                                      socials,
                                                      **validated_data)
        return questionnaire

    def update(self, instance, validated_data):
        teams = validated_data.pop('teams', None)
        toolkits = validated_data.pop('toolkit', None)
        projects = validated_data.pop('projects', None)
        accounts = validated_data.pop('accounts', None)
        user = validated_data.pop('user')
        languages = validated_data.pop('category', None)
        socials = validated_data.pop('socials', None)
        check_profile = services.check_profile(user, teams, projects, accounts, socials)
        if instance.avatar:
            instance.avatar.delete()
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
    toolkit = GetToolkitForUserSerializer(many=True)

    class Meta:
        model = models.Questionnaire
        fields = ('id', 'user', 'toolkit')


