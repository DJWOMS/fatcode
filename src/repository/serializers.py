from rest_framework import serializers

from . import models


class ProjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'name', 'parent']


class ProjectToolkitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Toolkit
        fields = ['id', 'name', 'parent']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = '__all__'


class ProjectUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    repository = serializers.CharField(required=False)

    class Meta:
        model = models.Project
        fields = ['name', 'description', 'repository']
