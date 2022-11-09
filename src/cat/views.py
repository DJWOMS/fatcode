from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from ..base.classes import MixedSerializer

from . import models
from . import serializers
from .permissions import IsInventoryCatUser, IsCatAuthUser


class ProductView(ListAPIView):
    queryset = models.Product.objects.select_related('category').all()
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ShopProductSerializer


class InventoryView(MixedSerializer, ModelViewSet):
    permission_classes = (IsInventoryCatUser,)
    serializer_classes_by_action = {
        'create': serializers.CreateItemSerializer,
        'list': serializers.CatInventorySerializer,
        'update': serializers.UpdateInventoryItemSerializer
    }

    def get_queryset(self):
        item = models.Item.objects.select_related('product', 'inventory').all()
        return (
            models.Inventory.objects.filter(pk=self.kwargs['pk'])
            .select_related('cat')
            .prefetch_related(Prefetch('item', queryset=item))
            .all()
        )


class HintView(CreateAPIView):
    queryset = models.Hint.objects.select_related('lesson', 'cat').all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.HintSerializer


class PhraseView(ListAPIView):
    queryset = models.Phrase.objects.select_related('cat').all()
    serializer_class = serializers.PhraseSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("name",)


class CatView(ReadOnlyModelViewSet):
    queryset = models.Cat.objects.select_related('user').all()
    serializer_class = serializers.CatSerializer


class CatUserView(ListAPIView):
    serializer_class = serializers.CatSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return models.Cat.objects.filter(user=self.request.user).select_related('user').all()


class UpdateCatUserView(UpdateAPIView):
    queryset = models.Cat.objects.select_related('user').all()
    serializer_class = serializers.CatSerializer
    permission_classes = (IsAuthenticated, IsCatAuthUser)
