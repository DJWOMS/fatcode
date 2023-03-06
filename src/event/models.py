from django.db import models


class Event(models.Model):
    """Модель событий"""
    name = models.CharField(max_length=50)
    date = models.DateTimeField()
    user = models.ForeignKey('profiles.FatUser', on_delete=models.CASCADE, related_name='events')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name