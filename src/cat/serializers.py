from rest_framework import serializers
from . import models
from .services import CatService


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


class PublicCatSerializer(serializers.ModelSerializer):
    inventory = CatInventorySerializer()

    class Meta:
        model = models.Cat
        fields = ('name', 'color', 'hungry', 'xp', 'level', 'avatar', 'die', 'help_count')


class CreateItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Item
        fields = ('quantity', 'product')

    def create(self, validated_data):
        url_params = self.context.get('request').parser_context.get('kwargs')
        inventory = models.Inventory.objects.get(id=url_params['id'])
        service = CatService(inventory.cat)
        try:
            item = service.buy_item(validated_data['product'], abs(validated_data['quantity']))
        except ValueError:
            raise serializers.ValidationError('Недостаточно средств')
        return item


class HintSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Hint
        fields = ('text', )

