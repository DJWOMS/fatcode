from django.contrib import admin

from src.repository import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    search_fields = ['name', 'id']


@admin.register(models.Toolkit)
class ToolkitAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    search_fields = ['name', 'id']


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'category', 'id']
    list_filter = ['name', 'user', 'category', 'toolkit__name']
    search_fields = ['name', 'id']

@admin.register(models.ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'project']
    search_fields = ['user', 'project']

