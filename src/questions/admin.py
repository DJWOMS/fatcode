from django.contrib import admin
from .models import Question, Tag

admin.site.register(Question)
admin.site.register(Tag)
