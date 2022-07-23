from src.profiles import models, serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response


class UserFatView(ModelViewSet):
    """Internal user display"""

    serializer_class = serializers.UserFatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.FatUser.objects.filter(id=self.request.user.id)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserFatPublicView(ModelViewSet):
    """Public user display"""

    queryset = models.FatUser.objects.all()
    serializer_class = serializers.UserFatPublicSerializer
    permission_classes = [permissions.AllowAny]


class ListSocialView(ListAPIView):
    queryset = models.Social.objects.all()
    serializer_class = serializers.ListSocialSerializer


class DetailSocialView(RetrieveAPIView):
    queryset = models.Social.objects.all()
    serializer_class = serializers.ListSocialSerializer
    lookup_field = 'id'



