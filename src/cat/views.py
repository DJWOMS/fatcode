from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from . import models
from . import serializers
from rest_framework.permissions import IsAuthenticated
from .permissions import IsCatUser


class CheckInventoryView(RetrieveAPIView):
    queryset = models.Inventory.objects.all()
    serializer_class = serializers.CatInventorySerializer
    permission_classes = [IsCatUser]
    lookup_field = 'id'


class CheckShopView(ListAPIView):
    queryset = models.Product.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ShopProductSerializer


class BuyItemView(CreateAPIView):
    queryset = models.Item.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = []