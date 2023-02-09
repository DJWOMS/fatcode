from rest_framework import serializers

from src.profiles import services as services_profile
from src.questionnaire import models
from src.team import services as services_team
from src.repository import services as services_rep
from src.profiles import serializers as profile_serializers
from src.team.serializers import TeamsSerializer
from src.repository.serializers import UsersProjectsSerializer, UsersToolkitSerializer

from . import services


class QuestionnaireListSerializer(serializers.ModelSerializer):
    """Сериализатор списка анкет"""
    user = profile_serializers.GetUserSerializer()
    toolkits = UsersToolkitSerializer(many=True)

    class Meta:
        model = models.Questionnaire
        fields = ('id', 'user', 'toolkits')


class QuestionnaireDetailSerializer(serializers.ModelSerializer):
    """Сериализатор анкеты пользователя"""
    projects = UsersProjectsSerializer(many=True)
    toolkits = UsersToolkitSerializer(many=True)
    teams = TeamsSerializer(many=True)
    accounts = profile_serializers.AccountsSerializer(many=True)
    languages = profile_serializers.LanguagesSerializer(many=True)
    socials = profile_serializers.SocialsSerializer(many=True)
    user = profile_serializers.UserFieldsSerializer()

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
        services_profile.check_socials(user, socials)
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
    projects = UsersProjectsSerializer(many=True)

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
    accounts = profile_serializers.AccountsSerializer(many=True)

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
        services_profile.check_account(accounts, user)
        instance = services.questionnaire_update_accounts(instance, accounts)
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


class AdditionallyProfileSerializer(serializers.ModelSerializer):
    """Сериализатор представление профиля для автора"""
    toolkits = UsersToolkitSerializer(many=True)
    languages = profile_serializers.LanguagesSerializer(many=True)
    user = profile_serializers.GetUserForProjectSerializer()

    class Meta:
        model = models.Questionnaire
        fields = ('user', 'description', 'country', 'town', 'phone', 'birthday', 'avatar', 'toolkits', 'languages')