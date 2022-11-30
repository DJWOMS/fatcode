from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from ..base.classes import MixedSerializer

from . import models, serializers
from .filters import ArticleFilter


class CategoryView(ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class TagListView(ListAPIView):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer


class ArticleView(MixedSerializer, ModelViewSet):
    queryset = (
        models.Article.objects
        .filter(published=True)
        .select_related("author")
        .prefetch_related("tag", "category", "glossary")
    )
    serializer_classes_by_action = {
        'list': serializers.ListArticleSerializer,
        'retrieve': serializers.DetailArticleSerializer,
    }
    # pagination_class = ListArticleViewPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    filterset_class = ArticleFilter
    search_fields = ['title']


class GlossaryLetterListView(ListAPIView):
    queryset = models.Glossary.objects.all()
    serializer_class = serializers.GlossaryLetterSerializer


class GlossaryArticleListView(ListAPIView):
    serializer_class = serializers.GlossaryArticleSerializer

    def get_queryset(self):
        letter = self.request.query_params.get('letter')
        if letter is not None:
            return models.Article.objects.filter(published=True, glossary__letter=letter)
