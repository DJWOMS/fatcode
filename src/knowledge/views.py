from rest_framework.generics import ListAPIView, RetrieveAPIView
from src.knowledge import models, serializers


class ListCategoryView(ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class DetailCategoryView(RetrieveAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    lookup_field = 'id'


class ListTagView(ListAPIView):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer


class DetailTagView(RetrieveAPIView):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    lookup_field = 'id'


class ListArticleView(ListAPIView):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ListArticleSerializer


class DetailArticleView(RetrieveAPIView):
    queryset = models.Article.objects.all()
    serializer_class = serializers.DetailArticleSerializer
    lookup_field = 'id'
