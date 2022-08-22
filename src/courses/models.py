from django.db import models
from django.conf import settings
from .services import check_quiz, check_code


class Tags(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=30)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    slug = models.SlugField()
    view_count = models.IntegerField(editable=False, default=0)
    published = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='author'
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='UserCourseThrough',
        related_name='students'
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        related_name='mentor',
        null=True,
        blank=True
    )
    tags = models.ManyToManyField(Tags)

    def __str__(self):
        return self.name

    def all_lessons(self):
        return Lesson.objects.filter(course=self)

    def students_count(self):
        return UserCourseThrough.objects.filter(course=self).count()


class Lesson(models.Model):
    LESSON_CHOISE = (
        ('quiz', 'Квиз'),
        ('python', 'Python'),
        ('sql', 'SQL'),
        ('js', 'JavaScript'),
        ('html', 'HTML'),
        ('css', 'CSS')
    )
    lesson_type = models.CharField(max_length=500, choices=LESSON_CHOISE)
    name = models.CharField(max_length=500)
    viewed = models.IntegerField(default=0, editable=False)
    hint = models.TextField(null=True, blank=True)
    video_url = models.URLField(max_length=500, null=True, blank=True)
    published = models.DateField(auto_now_add=True)
    sorted = models.IntegerField(default=1)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    slug = models.SlugField()
    description = models.TextField()

    class Meta:
        ordering = ['sorted']

    def __str__(self):
        return self.name


class Quiz(models.Model):
    text = models.TextField()
    right = models.BooleanField(default=False)
    hint = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quiz')


class StudentWork(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='work'
    )
    completed = models.BooleanField(default=False)
    code_answer = models.TextField(null=True, blank=True)
    quiz_answer = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.quiz_answer:
            self.completed = check_quiz()
        if self.code_answer:
            self.completed = check_code()
        return super().save()


class UserCourseThrough(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='student')
    progress = models.IntegerField(default=0)

    def clean_progress(self):
        self.progress = 0
        return self.save()

    def update_progress(self):
        completed_work = StudentWork.objects.filter(student=self.student, completed=True).count()
        self.progress = int(completed_work / self.course.all_lessons().count() * 100)
        return self.save()


class CodeQuestion(models.Model):
    code = models.TextField()
    answer = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='code')


class HelpUser(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    mentor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='help_mentor')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Студенту {self.student} нужна помощь на уроке {self.lesson.name}"
