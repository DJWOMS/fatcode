from django.db import models
from django.utils import timezone

from src.profiles.models import FatUser
from src.repository.models import Project


class Board(models.Model):
    """ Модель доски заданий
    """
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='board')
    user = models.ForeignKey(FatUser, on_delete=models.CASCADE, related_name='boards')
    title = models.CharField(max_length=50, blank=True, null=True)


class Column(models.Model):
    """ Модель столбцов в доске заданий
    """
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='columns')
    position = models.IntegerField(default=0)
    title = models.CharField(max_length=50)


class Card(models.Model):
    """ Модель карточек в доске заданий
    """
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='cards')
    position = models.IntegerField(default=0)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=timezone.now)
    labels = models.ManyToManyField('Label', blank=True, null=True)
    members = models.ManyToManyField(FatUser, related_name='cards_member', blank=True, null=True)


class Label(models.Model):
    """ Модель меток в доске заданий
    """
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='labels')
    title = models.CharField(max_length=50)
    color = models.CharField(max_length=20)
