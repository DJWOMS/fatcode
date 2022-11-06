from django.contrib import admin

from src.repository.models import Category, Toolkit, Project


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    search_fields = ['name', 'id']


@admin.register(Toolkit)
class ToolkitAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    search_fields = ['name', 'id']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'category', 'id']
    list_filter = ['name', 'user', 'category', 'toolkit__name']
    search_fields = ['name', 'id']
