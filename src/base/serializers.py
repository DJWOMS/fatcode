from rest_framework import serializers


class FilterCommentListSerializer(serializers.ListSerializer):
    """ Фильтр комментариев, только parents """

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)
