from rest_framework import serializers, exceptions

from . import models
from ..profiles.serializers import GetUserSerializer
from ..team.models import TeamMember


class CardMixin:

    def set_members(self, instance, data_members):
        for member in data_members:
            try:
                TeamMember.objects.get(
                    user_id=member.get('id'), team=instance.listId.boardId.project.team
                )
            except TeamMember.DoesNotExist:
                raise exceptions.ValidationError(
                    detail=f"Member {member.get('username')} not found", code=404
                )
            instance.members.add(member.get('id'))

    def set_labels(self, instance, data_labels):
        for label in data_labels:
            add_label, _ = models.Label.objects.get_or_create(
                id=label.get('id'), boardId_id=label.get('boardId'), title=label.get('title')
            )
            instance.labels.add(add_label)


class ProfileForCardSerializer(serializers.Serializer):
    """Profile serializer for cards of board serializer"""
    id = serializers.IntegerField()
    username = serializers.CharField()
    avatar = serializers.ImageField(read_only=True)


class LabelForCreateCardSerializer(serializers.Serializer):
    """Label serializer for cards of board serializer"""
    id = serializers.IntegerField(required=False)
    boardId = serializers.IntegerField(write_only=True)
    title = serializers.CharField()


class LabelForUpdateCardSerializer(serializers.ModelSerializer):
    """Serializer Label доски заданий"""
    id = serializers.IntegerField()

    class Meta:
        model = models.Label
        fields = ('id', 'board', 'title')


class LabelSerializer(serializers.ModelSerializer):
    """Serializer Label доски заданий"""

    class Meta:
        model = models.Label
        fields = ('id', 'board', 'title')


class SetCardSerializer(CardMixin, serializers.ModelSerializer):
    """Serializer Card доски заданий"""
    labels = LabelForCreateCardSerializer(many=True)
    members = ProfileForCardSerializer(many=True)
    board = serializers.SerializerMethodField('get_board_id', read_only=True)

    def get_board_id(self, obj):
        return obj.listId.board.id

    class Meta:
        model = models.Card
        fields = (
            'id',
            'column',
            'position',
            'title',
            'description',
            'create_date',
            'due_date',
            'labels',
            'members',
            'board'
        )

    def create(self, validated_data):
        data_members = validated_data.pop('members')
        data_labels = validated_data.pop('labels')
        instance = models.Card.objects.create(**validated_data)
        self.set_members(instance, data_members)
        self.set_labels(instance, data_labels)
        return instance


class UpdateCardSerializer(CardMixin, serializers.ModelSerializer):
    """Serializer Card доски заданий"""
    labels = LabelForUpdateCardSerializer(many=True)
    members = ProfileForCardSerializer(many=True)

    class Meta:
        model = models.Card
        fields = (
            'id',
            'column',
            'position',
            'title',
            'description',
            'create_date',
            'due_date',
            'labels',
            'members'
        )

    def update(self, instance, validated_data):
        data_members = validated_data.pop('members')
        data_labels = validated_data.pop('labels')
        instance = super().update(instance, validated_data)
        instance.members.clear()
        instance.labels.clear()
        self.set_members(instance, data_members)
        self.set_labels(instance, data_labels)
        return instance


class GetCardSerializer(serializers.ModelSerializer):
    """Serializer Card доски заданий"""
    members = GetUserSerializer(many=True)
    labels = LabelSerializer(many=True)
    board = serializers.SerializerMethodField('get_board_id')

    def get_board_id(self, obj):
        return obj.listId.board.id

    class Meta:
        model = models.Card
        fields = (
            'id',
            'column',
            'position',
            'title',
            'description',
            'create_date',
            'due_date',
            'labels',
            'members',
            'board'
        )


class SetColumnSerializer(serializers.ModelSerializer):
    """Serializer Column доски заданий"""
    class Meta:
        model = models.Column
        fields = ('id', 'board', 'position', 'title')


class UpdateColumnSerializer(serializers.ModelSerializer):
    """Serializer update Column доски заданий"""
    cards = GetCardSerializer(many=True, read_only=True)

    class Meta:
        model = models.Column
        fields = ('id', 'board', 'position', 'title', 'cards')

    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        instance.position = validated_data['position']
        instance.save()
        return instance


class GetColumnSerializer(serializers.ModelSerializer):
    """Serializer Column доски заданий"""
    cards = GetCardSerializer(many=True, read_only=True)

    class Meta:
        model = models.Column
        fields = ('id', 'board', 'position', 'title', 'cards')


class SetBoardSerializer(serializers.ModelSerializer):
    """Serializer доски заданий"""
    columns = GetColumnSerializer(many=True, read_only=True)
    labels = LabelSerializer(many=True, read_only=True)

    class Meta:
        model = models.Board
        fields = ('id', 'title', 'columns', 'labels')


class GetBoardSerializer(serializers.ModelSerializer):
    """Serializer доски заданий"""
    columns = GetColumnSerializer(many=True)
    labels = LabelSerializer(many=True)

    class Meta:
        model = models.Board
        fields = ('id', 'project', 'title', 'columns', 'labels')
