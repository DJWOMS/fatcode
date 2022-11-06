from rest_framework import serializers

from . import models

from ..profiles.serializers import GetUserSerializer
from ..team.serializers import GetTeamSerializer


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
            'repository'
        )


class ProjectListSerializer(serializers.ModelSerializer):
    """Список проектов"""
    user = GetUserSerializer()
    category = CategorySerializer()
    toolkit = ToolkitSerializer(many=True)

    class Meta:
        model = models.Project
        fields = (
            'id',
            'name',
            'description',
            'create_date',
            'user',
            'avatar',
            'toolkit',
            'category'
        )


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Проект детально"""
    user = GetUserSerializer()
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
