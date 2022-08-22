from django_filters import rest_framework as filters
from .models import Article


class ArticleFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='category', lookup_expr='icontains')
    date_creation = filters.CharFilter(field_name='date_creation', lookup_expr='year')

    class Meta:
        model = Article
        fields = ['category', 'date_creation']
