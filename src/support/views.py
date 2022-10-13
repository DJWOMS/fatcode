from rest_framework import parsers
from rest_framework.viewsets import ModelViewSet

from .models import Report
from .serializers import (
    ReportDetailSerializer,
    ReportListSerializer,
    ReportCreateSerializer
)

from ..base.classes import MixedSerializer
from ..base.permissions import IsAuthor


class ReportView(MixedSerializer, ModelViewSet):
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = (IsAuthor,)
    serializer_classes_by_action = {
        'list': ReportListSerializer,
        'retrieve': ReportDetailSerializer,
        'create': ReportCreateSerializer
    }

    def get_queryset(self):
        return Report.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
