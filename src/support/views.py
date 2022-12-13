from rest_framework import parsers
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from ..base.classes import MixedSerializer
from ..base.permissions import IsUser

from . import serializers
from .models import Report, Category


class CategoryView(ReadOnlyModelViewSet):
    """Категории"""
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class ReportView(MixedSerializer, ModelViewSet):
    """CR отчета"""
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = (IsUser,)
    serializer_classes_by_action = {
        'list': serializers.ReportListSerializer,
        'retrieve': serializers.ReportDetailSerializer,
        'create': serializers.ReportCreateSerializer
    }

    def get_queryset(self):
        return Report.objects.select_related("user", "category").filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
