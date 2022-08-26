from django.contrib import admin
from src.knowledge.models import Category, Tag, Article
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ArticleAdminForm(forms.ModelForm):
    """Form for connecting ckeditor to Article model"""

    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Article
        fields = '__all__'


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ('title', 'author', 'published', 'date_creation')
    list_filter = ('author', 'category', 'published')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
