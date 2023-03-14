from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from src.base.classes import MixedPermissionSerializer

from . import serializers, models
from ..base.permissions import IsUser


class EventView(MixedPermissionSerializer, viewsets.ModelViewSet):
    """ CRUD событий """

    permission_classes_by_action = {
        'list': (IsAuthenticated, IsUser,),
        'create': (IsAuthenticated,),
        'retrieve': (IsAuthenticated, IsUser,),
        'update': (IsAuthenticated, IsUser,),
        'destroy': (IsAuthenticated, IsUser,)
    }
    serializer_classes_by_action = {
        'list': serializers.EventSerializers,
        'retrieve': serializers.EventSerializers,
        'create': serializers.EventSerializers,
        'update': serializers.EventSerializers,
        'destroy': serializers.EventSerializers
    }

    def get_queryset(self):
        return models.Event.objects.select_related('user').filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()
