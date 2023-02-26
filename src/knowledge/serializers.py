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
    tags = TagSerializer(many=True)
    like_count = serializers.IntegerField()
    dislike_count = serializers.IntegerField()

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
            'tags',
            'video_url',
            'like_count',
            'dislike_count'
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


class CommentListSerializer(serializers.ModelSerializer):
    """Сериализатор вывода списка комментариев"""
    user = GetUserSerializer()

    class Meta:
        model = models.CommentArticle
        fields = ("id", "user", "text", "create_date")
        ref_name = 'comment_list_knowledge'


class CUDCommentSerializer(serializers.ModelSerializer):
    """Сериализатор CUD комментариев к article"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.CommentArticle
        fields = ("text", "user")


class LikeSerializer(serializers.ModelSerializer):
    """Сериализатор лайков"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.LikeDislike
        fields = ("id", "user", "status", "create_date")
