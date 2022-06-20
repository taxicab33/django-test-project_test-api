from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from api.custom_permissions import IsOwner
from api.newsapp.serializers import ArticleSerializer
from api.newsapp.utils import ArticlesAPIListPagination
from newsapp.models import Article
from newsapp.utils import DataMixin


class ArticlesAPIList(generics.ListCreateAPIView, DataMixin):
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = ArticlesAPIListPagination

    def get_queryset(self):
        queryset = self.get_sorted_articles()
        return queryset


class ArticleDetailAPIView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ArticleUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsOwner, )
