from rest_framework import serializers
from . import models


class PublicCatSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Cat
        fields = ('name', 'color')


class ShopProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Product
        fields = '__all__'


class InventoryProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Product
        fields = ('name', 'image', 'genus', 'category')


class InventoryItemSerializer(serializers.ModelSerializer):
    product = InventoryProductSerializer()

    class Meta:
        model = models.Item
        fields = ('product', 'quantity')


class CatInventorySerializer(serializers.ModelSerializer):
    item = InventoryItemSerializer(many=True)

    class Meta:
        model = models.Inventory
        fields = ('item', )
        read_only_fields = ('cat', )


class PublicItemSerializer(serializers.ModelSerializer):
    cat = PublicCatSerializer()
    inventory = CatInventorySerializer()

    class Meta:
        models = models.Item
        fields = ('product', 'quantity', 'inventory')


