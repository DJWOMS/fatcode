from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from . import models
from . import serializers
from .permissions import IsInventoryCatUser
from ..base.classes import MixedSerializer


class ProductView(ListAPIView):
    queryset = models.Product.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ShopProductSerializer


class InventoryView(MixedSerializer, ModelViewSet):
    lookup_field = 'id'
    queryset = models.Inventory.objects.all()
    permission_classes = [IsInventoryCatUser]
    serializer_classes_by_action = {
        'create': serializers.CreateItemSerializer,
        'list': serializers.CatInventorySerializer,
        'update': serializers.UpdateInventoryItemSerializer
    }

    def get_queryset(self):
        queryset = models.Inventory.objects.filter(id=self.kwargs['id'])
        return queryset


class HintView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.HintSerializer


class PhraseView(ListAPIView):
    queryset = models.Phrase.objects.all()
    serializer_class = serializers.PhraseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ["name", ]
