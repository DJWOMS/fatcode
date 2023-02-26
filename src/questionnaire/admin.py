from django.contrib import admin
from . import models


@admin.register(models.Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('user', 'description')
    search_fields = ('user', )


