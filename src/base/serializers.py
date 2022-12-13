from rest_framework import serializers


class FilterCommentListSerializer(serializers.ListSerializer):
    """ Фильтр комментариев, только parents """

    def to_representation(self, data):
        return super().to_representation(data)
