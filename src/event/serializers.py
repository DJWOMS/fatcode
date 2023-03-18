import datetime

from django.utils import timezone
from rest_framework import serializers

from .models import Event
from . import services


class EventSerializers(serializers.ModelSerializer):
    """Сериализатор просмотра событий"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Event
        fields = ("id", "name", "date", "user")

    def create(self, validated_data):
        date = validated_data.pop('date')
        _date = services.check_date(validated_data.get('user'), date)
        event = Event.objects.create(
            date=_date,
            **validated_data
        )
        return event

    def update(self, instance, validated_data):
        date = validated_data.pop('date')
        _date = services.check_date(validated_data.get('user'), date)
        instance.date = _date
        instance.save()
        return instance