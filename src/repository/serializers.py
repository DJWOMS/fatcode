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
        repository = validated_data.get('repository', None)
        nik = services.get_nik(validated_data.get('user'))
        if nik:
            repo = services.get_my_repository(repository, nik)
            if repo:
                try:
                    for team in validated_data.get('teams'):
                        team = Team.objects.get(
                            Q(user=validated_data.get('user').id) &
                            Q(id=team.id)
                        )
                except Team.DoesNotExist:
                    raise APIException(
                        detail='Создать возможно только для своей команды',
                        code=status.HTTP_400_BAD_REQUEST
                    )
            else:
                raise APIException(
                    detail='Добавить репозиторий возможно только для своего аккаунта',
                    code=status.HTTP_400_BAD_REQUEST
                )
            stars_count = services.get_stars_count(nik, repo)
            forks_count = services.get_forks_count(nik, repo)
            commits_count = services.get_commits_count(nik, repo)
            last_commit = services.get_last_commit(nik, repo)
        else:
            raise APIException(
                detail='Добавить репозиторий возможно только для аккаунтов привязанных к github',
                code=status.HTTP_400_BAD_REQUEST
            )

        projects = models.Project.objects.create(
                name=validated_data.get('name', None),
                description=validated_data.get('description', None),
                user=validated_data.get('user', None),
                category=validated_data.get('category', None),
                avatar=validated_data.get('avatar', None),
                repository=validated_data.get('repository', None),
                star=stars_count,
                fork=forks_count,
                commit=commits_count,
                last_commit=last_commit
            )
        for team in validated_data.get('teams', None):
            projects.teams.add(team)
        for toolkit in validated_data.get('toolkit', None):
            projects.toolkit.add(toolkit)
        return projects

    def update(self, instance, validated_data):
        repository = validated_data.get('repository', None)
        nik = services.get_nik(validated_data.get('user'))
        repo = services.get_my_repository(repository, nik)
        if repo:
            try:
                for team in validated_data.get('teams'):
                    team = Team.objects.get(
                        Q(user=validated_data.get('user').id) &
                        Q(id=team.id)
                    )
            except Team.DoesNotExist:
                raise APIException(
                    detail='Создать возможно только для своей команды',
                    code=status.HTTP_400_BAD_REQUEST
                )
        else:
            raise APIException(
                detail='Добавить репозиторий возможно только для своего аккаунта',
                code=status.HTTP_400_BAD_REQUEST
            )
        stars_count = services.get_stars_count(nik, repo)
        forks_count = services.get_forks_count(nik, repo)
        commits_count = services.get_commits_count(nik, repo)
        last_commit = services.get_last_commit(nik, repo)
        instance.name = validated_data.get('name', None)
        instance.description = validated_data.get('description', None)
        instance.avatar = validated_data.get('avatar', None)
        instance.category = validated_data.get('category', None)
        for team in validated_data.get('teams', None):
            instance.teams.add(team)
        for toolkit in validated_data.get('toolkit', None):
            instance.toolkit.add(toolkit)
        instance.repository = validated_data.get('repository', None)
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