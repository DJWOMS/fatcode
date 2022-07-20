from django.contrib import admin
from src.knowledge.models import Category, Tag, Article

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Tag)
