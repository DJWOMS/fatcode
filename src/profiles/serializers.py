from djoser.serializers import UserSerializer, UserCreatePasswordRetypeSerializer
from djoser.conf import settings
from rest_framework import serializers

from src.base.validators import ImageValidator
from src.base import exceptions

from src.profiles import models, services

from src.repository.models import Toolkit, Project
from src.team.models import Team
from src.profiles import models
from src.team import services as services_team
from src.repository import services as services_rep
from src.base.validators import ImageValidator
from src.profiles.services import add_friend


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


class ProjectsSerializer(serializers.ModelSerializer):
    """Сериализатор проектов пользователя"""

    class Meta:
        model = Project
        fields = ('id', 'name')


class ToolkitSerializer(serializers.ModelSerializer):
    """Сериализатор инструментов пользователя"""

    class Meta:
        model = Toolkit
        fields = ('name',)



class TeamsSerializer(serializers.ModelSerializer):
    """Сериализатор команд пользователя"""

    class Meta:
        model = Team
        fields = ('name',)


class AccountsSerializer(serializers.ModelSerializer):
    """Сериализатор аккаунтов пользователя"""

    class Meta:
        model = models.Account
        fields = ('provider', 'account_url')


class LanguagesSerializer(serializers.ModelSerializer):
    """Сериализатор языков"""

    class Meta:
        model = models.Language
        fields = ('name',)


class SocialsSerializer(serializers.ModelSerializer):
    """Сериализатор социальных ссылок пользователя"""

    class Meta:
        model = models.FatUserSocial
        fields = ('full_social_link', )


class UserFieldsSerializer(serializers.ModelSerializer):
    """Сериализатор информации пользователя для анкеты"""

    class Meta:
        model = models.FatUser
        fields = ('username', 'full_name', 'email')


class QuestionnaireListSerializer(serializers.ModelSerializer):
    """Сериализатор списка анкет"""
    user = GetUserSerializer()
    toolkits = ToolkitSerializer(many=True)

    class Meta:
        model = models.Questionnaire
        fields = ('id', 'user', 'toolkits')


class QuestionnaireDetailSerializer(serializers.ModelSerializer):
    """Сериализатор анкеты пользователя"""
    projects = ProjectsSerializer(many=True)
    toolkits = ToolkitSerializer(many=True)
    teams = TeamsSerializer(many=True)
    accounts = AccountsSerializer(many=True)
    languages = LanguagesSerializer(many=True)
    socials = SocialsSerializer(many=True)
    user = UserFieldsSerializer()

    class Meta:
        model = models.Questionnaire
        fields = (
            "user",
            "avatar",
            "description",
            "country",
            "town",
            "phone",
            "birthday",
            "toolkits",
            "teams",
            "projects",
            "accounts",
            "socials",
            "languages"
        )


class CUDQuestionnaireSerializer(serializers.ModelSerializer):
    """Сериализатор создания анкеты пользователя"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Questionnaire
        fields = (
            "description",
            "country",
            "town",
            "phone",
            "birthday",
            "user",
            "toolkits",
            "teams",
            "projects",
            "accounts",
            "socials",
            "languages",
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

    # def update(self, instance, validated_data):
    #     teams = validated_data.pop('teams', None)
    #     toolkits = validated_data.pop('toolkits', None)
    #     projects = validated_data.pop('projects', None)
    #     accounts = validated_data.pop('accounts', None)
    #     user = validated_data.pop('user')
    #     languages = validated_data.pop('languages', None)
    #     socials = validated_data.pop('socials', None)
    #     services.check_profile(user, teams, projects, accounts, socials)
    #     instance = super().update(instance, validated_data)
    #     instance = services.questionnaire_update(instance, teams, toolkits, projects, accounts, languages, socials)
    #     instance.save()
    #     return instance


class UDQuestionnaireSerializer(serializers.ModelSerializer):
    """Сериализатор UD анкеты пользователя"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Questionnaire
        fields = (
            "description",
            "country",
            "town",
            "phone",
            "birthday",
            "user",
            "toolkits",
            "socials",
            "languages"
        )

    def update(self, instance, validated_data):
        # teams = validated_data.pop('teams', None)
        toolkits = validated_data.pop('toolkits', None)
        # projects = validated_data.pop('projects', None)
        # accounts = validated_data.pop('accounts', None)
        user = validated_data.pop('user')
        languages = validated_data.pop('languages', None)
        socials = validated_data.pop('socials', None)
        services.check_socials(user, socials)
        instance = super().update(instance, validated_data)
        instance = services.questionnaire_update(instance, toolkits, languages, socials)
        instance.save()
        return instance


class TeamsListQuestionnaireSerializer(serializers.ModelSerializer):
    """Сериализатор вывода команд для анкеты пользователя"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    teams = TeamsSerializer(many=True)

    class Meta:
        model = models.Questionnaire
        fields = ("teams", "user")


class UTeamsQuestionnaireSerializer(serializers.ModelSerializer):
    """Сериализатор обновления команд для анкеты пользователя"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Questionnaire
        fields = ("teams", "user")

    def update(self, instance, validated_data):
        teams = validated_data.pop('teams', None)
        user = validated_data.pop('user')
        services_team.check_teams(teams, user)
        instance = services.questionnaire_update_teams(instance, teams)
        instance.save()
        return instance


class ProjectsListQuestionnaireSerializer(serializers.ModelSerializer):
    """Сериализатор вывода проектов для анкеты пользователя"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    projects = ProjectsSerializer(many=True)

    class Meta:
        model = models.Questionnaire
        fields = ("projects", "user")


class UProjectsQuestionnaireSerializer(serializers.ModelSerializer):
    """Сериализатор обновления проектов для анкеты пользователя"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Questionnaire
        fields = ("projects", "user")

    def update(self, instance, validated_data):
        projects = validated_data.pop('projects', None)
        user = validated_data.pop('user')
        services_rep.check_projects(projects, user)
        instance = services.questionnaire_update_projects(instance, projects)
        instance.save()
        return instance


class AccountsListQuestionnaireSerializer(serializers.ModelSerializer):
    """Сериализатор вывода аккаунтов для анкеты пользователя"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    accounts = AccountsSerializer(many=True)

    class Meta:
        model = models.Questionnaire
        fields = ("accounts", "user")


class UAccountsQuestionnaireSerializer(serializers.ModelSerializer):
    """Сериализатор обновления аккаунтов для анкеты пользователя"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Questionnaire
        fields = ("accounts", "user")

    def update(self, instance, validated_data):
        accounts = validated_data.pop('accounts', None)
        user = validated_data.pop('user')
        services.check_account(accounts, user)
        instance = services.questionnaire_update_accounts(instance, accounts)
        instance.save()
        return instance


class ApplicationListSerializer(serializers.ModelSerializer):
    getter = GetUserSerializer()

    class Meta:
        model = models.Application
        fields = ('id', 'getter',)


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Application
        fields = ('id', 'getter',)


class FriendListSerializer(serializers.ModelSerializer):
    friend = GetUserSerializer()

    class Meta:
        model = models.Friend
        fields = ('id', 'friend',)

    def create(self, validated_data):
        return add_friend(friend=validated_data['friend'], user=validated_data['user'])


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Friend
        fields = ('id', 'friend',)

    def create(self, validated_data):
        return add_friend(friend=validated_data['friend'], user=validated_data['user'])


class AvatarProfileSerializer(serializers.ModelSerializer):
    """Сериализатор аватара профиля"""
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
    """Сериализатор аватара анкеты"""
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


class SocialProfileSerializer(serializers.ModelSerializer):
    """Сериализатор социальных ссылок профиля"""

    class Meta:
        model = models.Social
        fields = ('title',)


class SocialProfileSerializer(serializers.ModelSerializer):
    """Просмотр социальных ссылок профиля"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.FatUserSocial
        fields = ('id', 'full_social_link', 'user')


class SocialProfileCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания социальных ссылок профиля"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.FatUserSocial
        fields = ('id', 'social', 'user', 'user_url')

    def create(self, validated_data):
        user = validated_data.pop('user')
        social_link = validated_data.pop('social')
        user_url = validated_data.pop('user_url')
        return services.create_social(user, social_link, user_url)


class SocialProfileUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор обновления социальных ссылок профиля"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.FatUserSocial
        fields = ('id', 'user', 'user_url')

    def update(self, instance, validated_data):
        user_url = validated_data.pop('user_url')
        return services.check_or_update_social(instance, user_url)


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор представления профиля """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user_social = SocialProfileSerializer(many=True)

    class Meta:
        model = models.FatUser
        fields = ('id', 'username', 'avatar', 'full_name', 'email', 'user', 'user_social')


class UserProfileListSerializer(serializers.ModelSerializer):
    """Сериализатор представления пользователей """

    class Meta:
        model = models.FatUser
        fields = ('id', 'username', 'avatar', 'full_name', 'email')


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор RUDE профиля"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.FatUser
        fields = ('id', 'middle_name', 'email', 'user')

    def update(self, instance, validated_data):
        email = validated_data.pop('email', None)
        pk = validated_data.pop('pk')
        middle_name = validated_data.pop('middle_name', None)
        return services.check_or_update_email(instance, email, pk, middle_name)


class UserMeProfileSerializer(serializers.ModelSerializer):
    """Сериализатор профиля для user_me"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.FatUser
        fields = ('id', 'username', 'avatar', 'full_name', 'email', 'user', 'experience', 'coins')


class AdditionallyProfileSerializer(serializers.ModelSerializer):
    """Сериализатор представление профиля для автора"""
    toolkits = ToolkitSerializer(many=True)
    languages = LanguagesSerializer(many=True)
    user = GetUserForProjectSerializer()

    class Meta:
        model = models.Questionnaire
        fields = ('user', 'description', 'country', 'town', 'phone', 'birthday', 'avatar', 'toolkits', 'languages')


class SocialListSerializer(serializers.ModelSerializer):
    """Сериализатор социальных сетей"""

    class Meta:
        model = models.Social
        fields = ('title', 'logo', 'url')




# class UserSocialSerializer(serializers.ModelSerializer):
#     """Сериализатор социальных ссылок пользователя"""
#     class Meta:
#         model = models.FatUserSocial
#         fields = '__all__'

#
# class ListSocialSerializer(serializers.ModelSerializer):
#     """Сериализатор социальных ссылок"""
#     logo = serializers.ImageField(read_only=True)
#
#     class Meta:
#         model = models.Social
#         fields = '__all__'
#
#
# class UserAvatarSerializer(serializers.ModelSerializer):
#     """Update user avatar"""
#     avatar = serializers.ImageField(validators=[ImageValidator((100, 100), 1048576)])
#
#     class Meta:
#         model = models.FatUser
#         fields = [
#             "id",
#             "avatar"
#         ]
#
#
# class AccountSerializer(serializers.ModelSerializer):
#     """Serialization for user's git_hub account"""
#
#     class Meta:
#         model = models.Account
#         fields = ("account_url", )
#
#
# class UserSerializer(serializers.ModelSerializer):
#     """Serialization for user's internal display"""
#     email = serializers.EmailField(read_only=True)
#     avatar = serializers.ImageField(validators=[ImageValidator((100, 100), 1048576)])
#     user_social = UserSocialSerializer(many=True)
#     socials = ListSocialSerializer(many=True)
#     # courses = serializers.ListCourseSerializer(many=True)
#     user_account = AccountSerializer(read_only=True, many=True)
#
#     class Meta:
#         model = models.FatUser
#         exclude = (
#             "password",
#             "last_login",
#             "is_active",
#             "is_staff",
#             "is_superuser",
#             "groups",
#             "user_permissions"
#         )
#         ref_name = "Fat user"
#
#     def update(self, instance, validated_data):
#         if validated_data.get('user_social', None):
#             user_social = validated_data.pop('user_social')
#             self.update_user_social(instance, user_social)
#
#         return super().update(instance, validated_data)
#
#     def update_user_social(self, instance, user_social):
#         for soc in user_social:
#             entry_fatUserSocial = instance.user_social.filter(
#                 social=soc['social']).first()
#
#             if entry_fatUserSocial is not None:
#                 entry_fatUserSocial.user_url = soc['user_url']
#                 entry_fatUserSocial.save()
#             else:
#                 instance.user_social.create(social=soc['social'], user_url=soc['user_url'])

#
# class UserPublicSerializer(serializers.ModelSerializer):
#     """Serialization for public user display"""
#
#     avatar = serializers.ImageField(read_only=True)
#     user_social = UserSocialSerializer(many=True)
#     socials = ListSocialSerializer(many=True)
#     # courses = ListCourseSerializer(many=True)
#
#     class Meta:
#         model = models.FatUser
#         exclude = (
#             "email",
#             "password",
#             "last_login",
#             "is_active",
#             "is_staff",
#             "is_superuser",
#             "groups",
#             "user_permissions",
#         )


