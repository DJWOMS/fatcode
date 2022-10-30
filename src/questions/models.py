from django.core.validators import FileExtensionValidator
from django.db import models
from django.conf import settings

from src.base.validators import ImageValidator


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Question(models.Model):
    asked = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    title = models.CharField(max_length=150)
    viewed = models.IntegerField(default=0, editable=False)
    text = models.TextField()
    image = models.ImageField(
        upload_to="question/screens/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'png']),
            ImageValidator((250, 250), 524288)
        ]
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    tags = models.ManyToManyField(Tag)
    rating = models.IntegerField(editable=False, default=0)

    def __str__(self):
        return self.title


class Answer(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='answer'
    )
    text = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        upload_to="question/screens/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'png']),
            ImageValidator((250, 250), 524288)
        ]
    )
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    rating = models.IntegerField(editable=False, default=0)
    accepted = models.BooleanField(default=False, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

    def update_rating(self):
        self.rating += AnswerReview.objects.filter(answer=self, grade=True).count()
        self.rating -= AnswerReview.objects.filter(answer=self, grade=False).count()
        return super().save()


class QuestionReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    grade = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class AnswerReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    grade = models.BooleanField()
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='review')
