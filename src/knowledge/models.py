from django.db import models
from src.profiles.models import FatUser


class Category(models.Model):
    """Categories of articles"""

    name = models.CharField(max_length=50)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Article tags"""

    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Article(models.Model):
    """Knowledge Base Articles"""

    title = models.CharField(max_length=200)
    text = models.TextField(blank=True, null=True)
    published = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(FatUser, on_delete=models.SET_NULL, null=True)
    view_count = models.IntegerField(default=0)
    picture = models.ImageField(
        upload_to='article/picture',
        null=True,
        blank=True
    )
    category = models.ManyToManyField(
        Category,
        blank=True,
        related_name='article')
    tag = models.ManyToManyField(Tag, blank=True, related_name='article')
    video_url = models.URLField(max_length=500, null=True, blank=True)

    class Meta:
        ordering = ['date_creation']

    def __str__(self):
        return self.title
