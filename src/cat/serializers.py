from rest_framework import serializers
from . import models


class CatInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Inventory
        fields = ('items', )
        read_only_fields = ('cat', )
