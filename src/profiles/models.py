import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from src.profiles.validators import AvatarValidator
from src.courses.models import Course


def user_directory_path(instance: 'FatUser', filename: str):
    """File will be uploaded to MEDIA_ROOT/users/avatar/user_<id>/<filename>"""

    # return example a2fabc70-be8e-49ac-9a8f-95d36a893d3d.png
    return f'users/avatar/user_{instance.id}/' \
           f'{str(uuid.uuid4()) + "." + filename.split(".")[-1]}'


class Social(models.Model):
    """Social networks"""

    title = models.CharField(max_length=150)
    logo = models.ImageField(upload_to='social/logo', null=True, blank=True)
    url = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.title


class FatUser(AbstractUser):
    """User model override"""

    first_login = models.DateTimeField(null=True, blank=True)
    avatar = models.ImageField(
        upload_to=user_directory_path,
        null=True,
        blank=True,
        validators=[AvatarValidator()]
    )
    middle_name = models.CharField(max_length=150, null=True, blank=True)
    socials = models.ManyToManyField(Social, through='FatUserSocial')
    courses = models.ManyToManyField(Course, through='FatUserCourse')


class FatUserSocial(models.Model):
    """Intermediate table for the ManyToMany FatUser and Social relationship"""

    social = models.ForeignKey(Social, on_delete=models.CASCADE)
    user = models.ForeignKey(
        FatUser,
        on_delete=models.CASCADE,
        related_name='user_social')
    user_url = models.CharField(max_length=20, default='')


class FatUserCourse(models.Model):
    """Intermediate table for the ManyToMany FatUser and Course relationship"""

    STATUS = (
        ('in_process', 'in_process'),
        ('completed', 'completed')
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(
        FatUser,
        on_delete=models.CASCADE,
        related_name='user_courses')
    status = models.CharField(max_length=10, choices=STATUS, default='in_process')
