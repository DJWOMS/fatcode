from src.profiles.serializers import UserFatSerializer, UserFatPublicSerializer
from src.profiles.models import FatUser
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions


class UserFatView(ModelViewSet):
    """Internal user display"""

    serializer_class = UserFatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FatUser.objects.filter(id=self.request.user.id)


class UserFatPublicView(ModelViewSet):
    """Public user display"""

    queryset = FatUser.objects.all()
    serializer_class = UserFatPublicSerializer
    permission_classes = [permissions.AllowAny]



