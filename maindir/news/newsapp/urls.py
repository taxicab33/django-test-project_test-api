from django.urls import path

from .views import *

urlpatterns = [
    path('', ArticlesListView.as_view(), name='main'),
    path('main', ArticlesListView.as_view(), name='main'),
    path('article/<slug:article_slug>/', ArticleDetailView.as_view(), name='article'),
    path('category/<slug:cat_slug>/', ArticlesCategoryListView.as_view(), name='cat'),
    path('create_article/', CreateArticleView.as_view(), name='create_article'),
    path('article/<slug:article_slug>/update_article/', UpdateArticleView.as_view()),
    path('article/<slug:article_slug>/delete_article/', DeleteArticleView.as_view()),
]