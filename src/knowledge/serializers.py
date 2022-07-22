from rest_framework import serializers
from src.knowledge import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('id', 'name', 'parent', 'article')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ('id', 'name', 'article')


class ListArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        exclude = ['text']


class DetailArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = '__all__'
