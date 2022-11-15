from rest_framework import serializers

from . import models, services
from ..profiles.serializers import GetUserForProjectSerializer
from ..team.serializers import GetTeamSerializer
from ..team.models import Team
from ..dashboard.models import Board


class CategorySerializer(serializers.ModelSerializer):
    """Категории"""

    class Meta:
        model = models.Category
        fields = ('id', 'name', 'parent')


class ToolkitSerializer(serializers.ModelSerializer):
    """Инструментарий"""

    class Meta:
        model = models.Toolkit
        fields = ('id', 'name', 'parent')


class ProjectSerializer(serializers.ModelSerializer):
    """Проект"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Project
        fields = (
            'id',
            'name',
            'description',
            'avatar',
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
        projects = models.Project.objects.create(
                star=repo_info.stars_count,
                fork=repo_info.forks_count,
                commit=repo_info.commits_count,
                last_commit=repo_info.last_commit,
                user=user,
                repository=repository,
                **validated_data
            )
        for team in teams:
            projects.teams.add(team)
        for toolkit in toolkit:
            projects.toolkit.add(toolkit)
        return projects

    def update(self, instance, validated_data):
        pk = validated_data.pop('pk', None)
        repository = validated_data.pop('repository', None)
        teams = validated_data.pop('teams', None)
        user = validated_data.pop('user', None)
        account_id = services.get_info_for_user_update(repository, teams, user, pk)
        repo_info = services.get_repo(repository, account_id)
        instance = super().update(instance, validated_data)
        instance.teams.clear()
        instance.toolkit.clear()
        for team in teams:
            instance.teams.add(team)
        for toolkit in validated_data.get('toolkit', None):
            instance.toolkit.add(toolkit)
        instance.stars_count = repo_info.stars_count
        instance.forks_count = repo_info.forks_count
        instance.commits_count = repo_info.commits_count
        instance.last_commit = repo_info.last_commit
        instance.save()
        return instance


class ProjectUserListSerializer(serializers.ModelSerializer):
    """Список проектов пользователя"""
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


class ProjectListSerializer(serializers.ModelSerializer):
    """Список проектов"""
    category = CategorySerializer()
    toolkit = ToolkitSerializer(many=True)

    class Meta:
        model = models.Project
        fields = (
            'id',
            'name',
            'description',
            'create_date',
            'toolkit',
            'category',
            'star',
            'fork',
            'commit',
            'last_commit'
        )


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Проект детально"""
    user = GetUserForProjectSerializer()
    category = CategorySerializer()
    toolkit = ToolkitSerializer(many=True)
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
    """Список команд"""

    class Meta:
        model = Team
        fields = (
            'name',
        )


class ProjectBoardSerializer(serializers.ModelSerializer):
    """Доска задач"""
    user = GetUserForProjectSerializer()

    class Meta:
        model = Board
        fields = (
            'title',
            'user'
        )