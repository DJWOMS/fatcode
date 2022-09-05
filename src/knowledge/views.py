from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .filters import ArticleFilter
from .services import ListArticleViewPagination

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
    queryset = models.Article.objects.filter(published=True)
    serializer_class = serializers.ListArticleSerializer
    pagination_class = ListArticleViewPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ArticleFilter
    search_fields = ['title']


class DetailArticleView(RetrieveAPIView):
    queryset = models.Article.objects.filter(published=True)
    serializer_class = serializers.DetailArticleSerializer
    lookup_field = 'id'
