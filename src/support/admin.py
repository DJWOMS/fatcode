from django.contrib import admin

from .models import Report, Answer, Category


class AnswerTabInlines(admin.TabularInline):
    model = Answer
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    inlines = [AnswerTabInlines, ]
