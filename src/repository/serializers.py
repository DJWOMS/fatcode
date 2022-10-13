from rest_framework import serializers

from . import models
from ..profiles.serializers import GetUserSerializer
from ..team.serializers import GetTeamSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('id', 'name', 'parent')


class ToolkitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Toolkit
        fields = ('id', 'name', 'parent')


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Project
        fields = (
            'name',
            'description',
            'avatar',
            'toolkit',
            'category',
            'teams',
            'repository'
        )


class ProjectListSerializer(serializers.ModelSerializer):
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
    user = GetUserSerializer()
    category = CategorySerializer()
    toolkit = ToolkitSerializer(many=True)
    teams = GetTeamSerializer(many=True)

    class Meta:
        model = models.Project
        fields = '__all__'

