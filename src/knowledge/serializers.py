from rest_framework import serializers

from src.knowledge import models
from ..profiles.serializers import GetUserSerializer


class CategorySerializer(serializers.ModelSerializer):
    """Категории"""

    class Meta:
        model = models.Category
        fields = ('id', 'name', 'parent')
        ref_name = 'category_knowledge'


class TagSerializer(serializers.ModelSerializer):
    """Тэги"""

    class Meta:
        model = models.Tag
        fields = ('id', 'name')
        ref_name = 'tag_knowledge'


class ListArticleSerializer(serializers.ModelSerializer):
    """Список статей"""
    author = GetUserSerializer()

    class Meta:
        model = models.Article
        exclude = ('text', 'video_url')


class DetailArticleSerializer(serializers.ModelSerializer):
    """Статья детально"""
    author = GetUserSerializer()
    category = CategorySerializer(many=True)
    tag = TagSerializer(many=True)

    class Meta:
        model = models.Article
        fields = (
            'id',
            'title',
            'text',
            'published',
            'date_creation',
            'date_update',
            'author',
            'view_count',
            'picture',
            'category',
            'tag',
            'video_url'
        )


class GlossaryLetterSerializer(serializers.ModelSerializer):
    """Буква глоссария"""

    class Meta:
        model = models.Glossary
        fields = ("id", "letter")


class GlossaryArticleSerializer(serializers.ModelSerializer):
    """Статьи глоссария"""

    class Meta:
        model = models.Article
        fields = ("id", "title")
