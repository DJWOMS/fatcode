from rest_framework import serializers

from . import models, services
from ..profiles.serializers import GetUserForProjectSerializer
from ..team.serializers import GetTeamSerializer
from ..team.models import Team
from ..dashboard.models import Board


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор вывода категорий"""

    class Meta:
        model = models.Category
        fields = ('id', 'name', 'parent')


class ToolkitSerializer(serializers.ModelSerializer):
    """Сериализатор вывода инструментария"""

    class Meta:
        model = models.Toolkit
        fields = ('id', 'name', 'parent')


class GetCategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий для проекта"""

    class Meta:
        model = models.Category
        fields = ('id', 'name')


class GetToolkitSerializer(serializers.ModelSerializer):
    """Сериализатор инструментария для проекта"""

    class Meta:
        model = models.Toolkit
        fields = ('id', 'name')


class ProjectSerializer(serializers.ModelSerializer):
    """Сериализатор CU проекта"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Project
        fields = (
            'id',
            'name',
            'description',
            'toolkit',
            'category',
            'teams',
            'repository',
            'user'
        )

    def create(self, validated_data):
        repository = validated_data.pop('repository', None)
        teams = validated_data.pop('teams')
        toolkit = validated_data.pop('toolkit', None)
        user = validated_data.pop('user')
        account_id = services.get_info_for_user(repository, teams, user)
        repo_info = services.get_repo(repository, account_id)
        project = services.project_create(repo_info, user, repository, teams, toolkit, **validated_data)
        return project

    def update(self, instance, validated_data):
        pk = validated_data.pop('pk', None)
        repository = validated_data.pop('repository', None)
        teams = validated_data.pop('teams', None)
        user = validated_data.pop('user', None)
        toolkits = validated_data.pop('toolkit', None)
        account_id = services.get_info_for_user_update(repository, teams, user, pk)
        repo_info = services.get_repo(repository, account_id)
        instance = super().update(instance, validated_data)
        instance = services.project_update(instance, repo_info, teams, toolkits)
        instance.save()
        return instance


class ProjectUserListSerializer(serializers.ModelSerializer):
    """Сериализатор списока проектов"""
    category = CategorySerializer()
    toolkit = ToolkitSerializer(many=True)
    teams = GetTeamSerializer(many=True)

    class Meta:
        model = models.Project
        fields = (
            'id',
            'name',
            'description',
            'create_date',
            'toolkit',
            'category',
            'teams',
            'repository'
        )


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Сериализатор проекта детально"""
    user = GetUserForProjectSerializer()
    category = GetCategorySerializer()
    toolkit = GetToolkitSerializer(many=True)
    teams = GetTeamSerializer(many=True, read_only=True)

    class Meta:
        model = models.Project
        fields = (
            'id',
            'name',
            'description',
            'create_date',
            'user',
            'category',
            'toolkit',
            'teams',
            'avatar',
            'repository',
            'star',
            'fork',
            'commit',
            'last_commit'
        )


class ProjectTeamsSerializer(serializers.ModelSerializer):
    """Сериализатор списока команд"""

    class Meta:
        model = Team
        fields = (
            'name',
        )


class ProjectBoardSerializer(serializers.ModelSerializer):
    """Сериализатор доски задач"""
    user = GetUserForProjectSerializer()

    class Meta:
        model = Board
        fields = (
            'title',
            'user'
        )


class AvatarProjectSerializer(serializers.ModelSerializer):
    """Сериализатор аватара проекта"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Project
        fields = ('avatar', 'user')

    def update(self, instance, validated_data):
        if instance.avatar:
            instance.avatar.delete()
        instance = super().update(instance, validated_data)
        instance.save()
        return instance

