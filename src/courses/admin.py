from django.contrib import admin
from .models import *


class LessonTabInlines(admin.TabularInline):
    model = Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonTabInlines]

    class Meta:
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Tags)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)