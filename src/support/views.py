from rest_framework import parsers
from rest_framework.viewsets import ModelViewSet

from . import serializers
from .models import Report

from ..base.classes import MixedSerializer
from ..base.permissions import IsUser


class ReportView(MixedSerializer, ModelViewSet):
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = (IsUser,)
    serializer_classes_by_action = {
        'list': serializers.ReportListSerializer,
        'retrieve': serializers.ReportDetailSerializer,
        'create': serializers.ReportCreateSerializer
    }

    def get_queryset(self):
        return Report.objects.filter(user_id=self.request.user.id).select_related("user", "category")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
