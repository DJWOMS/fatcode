from django.contrib import admin
from .models import *


class LessonTabInlines(admin.TabularInline):
    model = Lesson
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonTabInlines]

    class Meta:
        fields = '__all__'


admin.site.register(Tags)
admin.site.register(Category)