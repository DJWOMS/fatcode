from rest_framework import serializers

from . import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'name', 'parent']


class ToolkitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Toolkit
        fields = ['id', 'name', 'parent']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = '__all__'


