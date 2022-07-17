import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


def avatar_validator(value):
    if value.file.image.size != FatUser.allowed_avatar_size:
        raise ValidationError('Неправильный размер изображения')


def user_directory_path(instance, filename):
    """file will be uploaded to MEDIA_ROOT/users/avatar/user_<id>/<filename>"""

    # return example a2fabc70-be8e-49ac-9a8f-95d36a893d3d.png
    return f'users/avatar/user_{instance.id}/' \
           f'{str(uuid.uuid4()) + "." + filename.split(".")[-1]}'


class Social(models.Model):
    """social networks"""

    title = models.CharField(max_length=150)
    logo = models.ImageField(upload_to='social/logo', null=True, blank=True)


class FatUser(AbstractUser):
    """user model override"""

    allowed_avatar_size = (100, 100)

    first_login = models.DateTimeField(null=True, blank=True)
    avatar = models.ImageField(upload_to=user_directory_path, null=True,
                               blank=True, validators=[avatar_validator])
    middle_name = models.CharField(max_length=150, null=True, blank=True)
    socials = models.ManyToManyField(Social, through='FatUserSocial')


class FatUserSocial(models.Model):
    """intermediate table for the ManyToMany FatUser and Social relationship"""

    social = models.ForeignKey(Social, on_delete=models.CASCADE)
    user = models.ForeignKey(FatUser, on_delete=models.CASCADE)
    url = models.CharField(max_length=250)
