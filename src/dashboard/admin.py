from django.contrib import admin

from . import models


@admin.register(models.Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'project')
