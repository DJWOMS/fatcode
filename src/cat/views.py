from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.viewsets import ModelViewSet
from . import models
from . import serializers
from rest_framework.permissions import IsAuthenticated
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
        'list':  serializers.CatInventorySerializer
    }

    def get_queryset(self):
        queryset = models.Inventory.objects.filter(id=self.kwargs['id'])
        return queryset


class HintView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.HintSerializer


