import django_filters

from newsapp.models import Article


class ArticlesFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Article
        fields = ['price', 'release_date']