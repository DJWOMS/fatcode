from django.db.models import Q
from rest_framework import serializers, status
from rest_framework.exceptions import APIException

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
        if nik := services.get_nik(user):
            repo_info = services.check_team(repository, nik, teams, user)
        else:
            raise APIException(
                detail='Добавить репозиторий возможно только для аккаунтов привязанных к github',
                code=status.HTTP_400_BAD_REQUEST
            )
        projects = models.Project.objects.create(
                star=repo_info.stars_count,
                fork=repo_info.forks_count,
                commit=repo_info.commits_count,
                last_commit=repo_info.last_commit,
                **validated_data
            )
        for team in teams:
            projects.teams.add(team)
        for toolkit in toolkit:
            projects.toolkit.add(toolkit)
        return projects

    def update(self, instance, validated_data):
        repository = validated_data.get('repository', None)
        nik = services.get_nik(validated_data.get('user'))
        repo_info = services.check_team(repository, nik, validated_data.get('teams'), validated_data.get('user'))
        instance.name = validated_data.get('name', None)
        instance.description = validated_data.get('description', None)
        instance.avatar = validated_data.get('avatar', None)
        instance.category = validated_data.get('category', None)
        for team in validated_data.get('teams', None):
            instance.teams.add(team)
        for toolkit in validated_data.get('toolkit', None):
            instance.toolkit.add(toolkit)
        instance.repository = validated_data.get('repository', None)
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