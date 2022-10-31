from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from . import models
from . import serializers
from .permissions import IsInventoryCatUser, IsCatAuthUser
from ..base.classes import MixedSerializer, MixedPermissionSerializer


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


class CatView(ReadOnlyModelViewSet):
    queryset = models.Cat.objects.select_related('user').all()
    serializer_class = serializers.CatSerializer


class CatUserView(ListAPIView):
    serializer_class = serializers.CatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Cat.objects.filter(user=self.request.user)


class UpdateCatUserView(UpdateAPIView):
    queryset = models.Cat.objects.all()
    serializer_class = serializers.CatSerializer
    permission_classes = [IsAuthenticated, IsCatAuthUser]