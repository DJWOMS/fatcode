from rest_framework import serializers

from . import models


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'name', 'parent']


class ToolkitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Toolkit
        fields = ['id', 'name', 'parent']


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = '__all__'


