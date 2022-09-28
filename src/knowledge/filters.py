from django_filters import rest_framework as filters

from .models import Article


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class ArticleFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='category__name', lookup_expr="icontains")
    date_creation = filters.CharFilter(field_name='date_creation', lookup_expr='year')
    tag = CharFilterInFilter(field_name="tag__name", lookup_expr="in")

    class Meta:
        model = Article
        fields = ['category', 'date_creation', 'tag']
