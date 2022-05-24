from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', NewsHome.as_view(), name='main'),
    path('article/<slug:article_slug>/', ShowArticle.as_view(), name='article'),
    path('category/<slug:cat_slug>/', ShowCategories.as_view(), name='cat'),
    path('create_article/', CreateArticle.as_view(), name='create_article'),
]