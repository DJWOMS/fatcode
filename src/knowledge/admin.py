from django.contrib import admin
from src.knowledge import models
from django import forms


class ArticleAdminForm(forms.ModelForm):
    """Form for connecting ckeditor to Article model"""

    class Meta:
        model = models.Article
        fields = '__all__'


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ('title', 'author', 'published', 'date_creation')
    list_filter = ('author', 'category', 'published')
    filter_horizontal = ('glossary',)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')


@admin.register(models.CommentArticle)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'create_date')


@admin.register(models.LikeDislike)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'create_date', 'status')


@admin.register(models.Glossary)
class GlossaryAdmin(admin.ModelAdmin):
    """Glossary"""
    pass


admin.site.register(models.Tag)
