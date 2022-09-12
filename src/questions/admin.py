from django.contrib import admin
from .models import Question, Tag, Answer


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Question)
admin.site.register(Tag)
