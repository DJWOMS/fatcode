from django.contrib import admin
from .models import *


class LessonTabInlines(admin.TabularInline):
    model = Lesson
    extra = 1


class QuizTabular(admin.TabularInline):
    model = Quiz
    extra = 3


class CodeTabular(admin.TabularInline):
    model = CodeQuestion
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonTabInlines]
    list_display = ('name', 'autor', 'mentor')
    ordering = ['published']

    class Meta:
        fields = '__all__'


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    inlines = [QuizTabular, CodeTabular]
    list_display = ('course', 'lesson_type')

    class Meta:
        fields = '__all__'


admin.site.register(Tags)
admin.site.register(Category)
