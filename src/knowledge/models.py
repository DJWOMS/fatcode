from django.db import models

from src.profiles.models import FatUser


class Category(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Glossary(models.Model):
    letter = models.CharField(max_length=1, unique=True)

    def __str__(self):
        return self.letter


class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(FatUser, on_delete=models.SET_NULL, null=True)
    view_count = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='article/picture', null=True, blank=True)
    category = models.ManyToManyField(Category, related_name='article')
    tag = models.ManyToManyField(Tag, blank=True, related_name='article')
    video_url = models.URLField(max_length=500, null=True, blank=True)
    glossary = models.ManyToManyField(Glossary, blank=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class CommentArticle(models.Model):
    """Модель комментариев"""
    text = models.TextField(max_length=512)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    is_publish = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    user = models.ForeignKey('profiles.FatUser', on_delete=models.CASCADE, related_name='article_comments')
    article = models.ForeignKey(Article, related_name="article_comments", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}'


