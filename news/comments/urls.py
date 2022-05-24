from django.urls import path
from .views import *

urlpatterns = [
    path('article/<slug:article_slug>/comment', CommentView.as_view(), name='create_comment'),
    path('article/<slug:article_slug>/delete_comment', CommentView.as_view(), name='delete_comment'),
    path('article/<slug:article_slug>/edit_comment', CommentView.as_view(), name='edit_comment'),
]