from django.urls import path
from .views import *

urlpatterns = [
    path('article/<slug:article_slug>/like', VotesView.as_view(), name='article_like'),
    path('article/<slug:article_slug>/dislike', VotesView.as_view(), name='article_dislike'),
]