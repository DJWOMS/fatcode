from rest_framework import serializers

from src.knowledge import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('id', 'name', 'parent')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ('id', 'name')
        ref_name = 'tag_knowledge'


class ListArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        exclude = ['text', 'video_url']


class CategoryArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'name']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FatUser
        fields = ['id', 'username']


class DetailArticleSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    category = CategoryArticleSerializer(many=True)
    tag = TagSerializer(many=True)

    class Meta:
        model = models.Article
        fields = [
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
        ]


class GlossaryLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Glossary
        fields = [
            "id",
            "letter",
        ]


class GlossaryArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = [
            "id",
            "title",
        ]
