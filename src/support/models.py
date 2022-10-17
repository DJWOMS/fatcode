from django.db import models
from django.core.validators import FileExtensionValidator

from .validators import validate_size_video

from src.profiles.models import FatUser


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Report(models.Model):
    STATUS_CHOICES = (
        ("новая", "Новая"),
        ("исполнена", "Исполнена")
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(FatUser, on_delete=models.CASCADE)
    text = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="новая")
    image = models.ImageField(upload_to="reports/images/", blank=True, null=True)
    video = models.FileField(
        upload_to="reports/videos/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=["mp4", "mov"]), validate_size_video
        ]
    )

    def __str__(self):
        return self.text


class Answer(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()

    def __str__(self):
        return self.text
