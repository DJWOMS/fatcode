from rest_framework import permissions, viewsets, exceptions, status

from . import models, serializers
from ..base.classes import MixedPermissionSerializer, MixedPermission, MixedSerializer
from .permissions import IsAuthorProject, IsMemberProject, IsAuthorBoard, IsMemberBoard


class BoardView(MixedPermissionSerializer, viewsets.ModelViewSet):
    permission_classes_by_action = {
        'create': (permissions.IsAuthenticated, IsAuthorProject),
        'retrieve': (permissions.IsAuthenticated, IsMemberProject)
    }
    serializer_classes_by_action = {
        'create': serializers.SetBoardSerializer,
        'retrieve': serializers.GetBoardSerializer
    }

    def create(self, request, *args, **kwargs):
        if models.Board.objects.filter(project_id=self.kwargs.get('project_id')).exists():
            raise exceptions.APIException(
                code=status.HTTP_400_BAD_REQUEST, detail="Доска уже создана"
            )
        return super().create(request, *args, **kwargs)

    def get_object(self):
        try:
            obj = models.Board.objects.prefetch_related('labels').get(
                project_id=self.kwargs.get('project_id')
            )
        except models.Board.DoesNotExist:
            raise exceptions.APIException(code=404, detail="Board no found")
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, project_id=self.kwargs.get('project_id'))


class LabelView(MixedPermission, viewsets.ModelViewSet):
    queryset = models.Label.objects.all()
    permission_classes_by_action = {
        'create': (permissions.IsAuthenticated, IsAuthorBoard),
        'update': (permissions.IsAuthenticated, IsAuthorBoard),
        'destroy': (permissions.IsAuthenticated, IsAuthorBoard),
        'list': (permissions.IsAuthenticated, IsMemberProject)
    }
    serializer_class = serializers.LabelSerializer


class ColumnView(MixedSerializer, viewsets.ModelViewSet):
    queryset = models.Column.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsAuthorBoard)
    serializer_class = serializers.SetColumnSerializer
    serializer_classes_by_action = {
        'create': serializers.SetColumnSerializer,
        'update': serializers.UpdateColumnSerializer
    }


class CardView(MixedSerializer, viewsets.ModelViewSet):
    queryset = models.Card.objects.select_related('listId__boardId').all()
    permission_classes = (permissions.IsAuthenticated, IsMemberBoard)
    serializer_classes_by_action = {
        'create': serializers.SetCardSerializer,
        'update': serializers.UpdateCardSerializer,
        'retrieve': serializers.GetCardSerializer
    }
