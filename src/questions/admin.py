from django.contrib import admin
from .models import Question, Tag, Answer, QuestionFollowers


@admin.register(Question)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')


admin.site.register(Tag)
admin.site.register(QuestionFollowers)
