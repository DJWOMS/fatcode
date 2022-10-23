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
        fields = ('id', 'product', 'quantity')


class CatInventorySerializer(serializers.ModelSerializer):
    item = InventoryItemSerializer(many=True)

    class Meta:
        model = models.Inventory
        fields = ('id', 'item',)
        read_only_fields = ('cat',)


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
    hint = serializers.SerializerMethodField()

    class Meta:
        model = models.Hint
        fields = ('lesson', 'cat', 'hint')

    def get_hint(self, instance):
        return instance.lesson.hint

    def validate(self, data):
        if self.context['request'].user != data['cat'].user:
            raise serializers.ValidationError('Не твой кот')
        if data['cat'].help_count > 0:
            return data
        raise serializers.ValidationError('У вас закончились подсказки')

    def create(self, validated_data):
        service = CatService(validated_data['cat'])
        return service.get_hint(validated_data['lesson'])


class UpdateInventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Inventory
        fields = ('item',)

    def update(self, instance, validated_data):
        service = CatService(instance.cat)
        return service.feed_cat(validated_data['item'][0])


class PhraseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Phrase
        fields = ("id", "name", "text", "cat")


class CatSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source="user.username", read_only=True)

    class Meta:
        model = models.Cat
        fields = ("id", "avatar", "name", "user_id", "username")


class UpdateCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cat
        fields = ('name',)

    def update(self, instance, validated_data):
        service = CatService(instance)
        return service.give_name(validated_data['name'])
