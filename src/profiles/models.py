from django.db import models
from django.contrib.auth.models import AbstractUser


class Social(models.Model):
    title = models.CharField(max_length=150)
    logo = models.ImageField(upload_to='social/logo', null=True, blank=True)


class FatUser(AbstractUser):
    first_login = models.DateTimeField(null=True)
    avatar = models.ImageField(upload_to='user/avatar', null=True, blank=True)
    middle_name = models.CharField(max_length=150)
    socials = models.ManyToManyField(Social, through='FatUserSocial')


class FatUserSocial(models.Model):
    social = models.ForeignKey(Social, on_delete=models.CASCADE)
    user = models.ForeignKey(FatUser, on_delete=models.CASCADE)
    url = models.CharField(max_length=250)

