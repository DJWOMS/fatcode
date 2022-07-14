from django.db import models
from django.conf import settings


class Tags(models.Model):
    name = models.CharField(max_length=500)


class Category(models.Model):
    name = models.CharField(max_length=500)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)


class Course(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField()
    slug = models.SlugField()
    view_count = models.IntegerField(editable=False)
    published = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='autor')
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, through='UserCourseThrough', related_name='students')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name='mentor')
    tags = models.ManyToManyField(Tags, null=True, blank=True)


class Lesson(models.Model):
    name = models.CharField(max_length=500)
    viewed = models.IntegerField(default=0)
    hint = models.TextField(null=True)
    video_url = models.URLField(max_length=500)
    published = models.DateField(auto_now_add=True)
    sorted = models.IntegerField(default=1)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    slug = models.SlugField()
    description = models.TextField()


class StudentWork(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    code = models.TextField(null=True, blank=True)
    quiz = models.TextField(null=True, blank=True)


class UserCourseThrough(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='student')
    progress = models.IntegerField(default=0)


class Quiz(models.Model):
    text = models.TextField()
    right = models.BooleanField()
    hint = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)


class CodeQuestion(models.Model):
    TYPE_CHOISE = (
        ('quiz', 'Квиз'),
        ('python', 'Python'),
        ('sql', 'SQL'),
        ('js', 'JavaScript'),
        ('html', 'HTML'),
        ('css', 'CSS')
    )
    code = models.TextField()
    answer = models.TextField()
    code_type = models.CharField(max_length=500, choices=TYPE_CHOISE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
