from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from ..base.classes import MixedSerializer, MixedPermissionSerializer, MixedPermission
from rest_framework.response import Response

from . import models, serializers, permissions
from .filters import ArticleFilter
from ..base.permissions import IsUser
from ..base.service import view_count


class CategoryView(ModelViewSet):
    """Представление категорий"""
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class TagListView(ListAPIView):
    """Представление тегов"""
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer


class ArticleView(MixedSerializer, ModelViewSet):
    """Представление просмотра статей"""
    queryset = (
        models.Article.objects
        .filter(published=True)
        .annotate(
            like_count=Count("likedislike", filter=Q(likedislike__status='Like'), distinct=True)
        )
        .annotate(
            dislike_count=Count("likedislike", filter=Q(likedislike__status='Dislike'), distinct=True)
        )
        .select_related("author")
        .prefetch_related("tags", "category", "glossary")
    )
    serializer_classes_by_action = {
        'list': serializers.ListArticleSerializer,
        'retrieve': serializers.DetailArticleSerializer,
    }
    # pagination_class = ListArticleViewPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    filterset_class = ArticleFilter
    search_fields = ['title']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance = view_count(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class GlossaryLetterListView(ListAPIView):
    """Представление оглавлений"""
    queryset = models.Glossary.objects.all()
    serializer_class = serializers.GlossaryLetterSerializer


class GlossaryArticleListView(ListAPIView):
    """Предаставление списка статей"""
    serializer_class = serializers.GlossaryArticleSerializer

    def get_queryset(self):
        letter = self.request.query_params.get('letter')
        if letter is not None:
            return models.Article.objects.filter(published=True, glossary__letter=letter)


class CommentsView(MixedPermissionSerializer, ModelViewSet):
    """CRUD комментариев к статьям"""
    permission_classes_by_action = {
        'list': (IsAuthenticated, ),
        'create': (IsAuthenticated, ),
        'update': (IsAuthenticated, IsUser),
        'retrieve': (IsAuthenticated, ),
        'destroy': (IsAuthenticated, IsUser)
    }
    serializer_classes_by_action = {
        'list': serializers.KnowledgeCommentListSerializer,
        'create': serializers.CUDCommentSerializer,
        'retrieve': serializers.KnowledgeCommentListSerializer,
        'update': serializers.CUDCommentSerializer,
        'destroy': serializers.CUDCommentSerializer
    }
    lookup_url_kwarg = 'comment_pk'

    def get_queryset(self):
        return models.CommentArticle.objects.filter(article_id=self.kwargs.get('pk')).select_related('user')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, article_id=self.kwargs.get('pk'))

    def perform_update(self, serializer):
        serializer.save(user=self.request.user, id=self.kwargs.get('comment_pk'))

    def perform_destroy(self, instance):
        instance.delete()


class LikeDislikeView(MixedPermission, ModelViewSet):
    """CRUD лайков к статьям"""
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'create': (IsAuthenticated, permissions.IsLikeNotExists),
        'update': (IsAuthenticated, IsUser),
    }
    serializer_class = serializers.LikeSerializer
    lookup_url_kwarg = 'like_pk'

    def get_queryset(self):
        return models.LikeDislike.objects.filter(article_id=self.kwargs.get('pk')).select_related('user')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, article_id=self.kwargs.get('pk'))

    def perform_update(self, serializer):
        serializer.save(user=self.request.user, id=self.kwargs.get('like_pk'))

    def perform_destroy(self, instance):
        instance.delete()
