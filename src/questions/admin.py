from django.contrib import admin
from .models import Question, Tag, Answer, QuestionFollowers


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(QuestionFollowers)
