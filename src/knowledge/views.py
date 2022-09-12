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


class GlossaryListView(ListAPIView):
    """Letter for article"""
    queryset = models.Glossary.objects.all()
    serializer_class = serializers.GlossaryLetterSerializer


class GlossaryArticleListView(ListAPIView):
    """Glossary article"""
    serializer_class = serializers.GlossaryArticleSerializer

    def get_queryset(self):
        letter = self.request.query_params.get('letter')
        if letter is not None:
            queryset = models.Article.objects.filter(
                published=True, glossary__letter=letter)
            return queryset
