from django.urls import path, include, re_path
from .account.views import UserArticlesAPIList, UserInfoAPIView
from .comments.views import CommentAPIView, CommentsAPIList
from .favorite.views import FavoriteAPIView
from .newsapp.views import *
from .votes.views import VoteAPIView

urlpatterns = [
    # ���������/��������������/�������� ������/������
    path('api/v1/articles/', ArticlesAPIList.as_view()),
    path('api/v1/category/<slug:cat_slug>/', ArticlesAPIList.as_view()),
    path('api/v1/articles/<int:pk>/update/', ArticleUpdateDestroyAPIView.as_view()),
    path('api/v1/articles/<int:pk>/delete/', ArticleUpdateDestroyAPIView.as_view()),
    path('api/v1/articles/<int:pk>/', ArticleDetailAPIView.as_view()),
    # ���������������� ������
    path('api/v1/user/<slug:user_slug>/favorite_articles/', UserArticlesAPIList.as_view()),
    path('api/v1/user/<slug:user_slug>/liked_articles/', UserArticlesAPIList.as_view()),
    path('api/v1/user/<slug:user_slug>/', UserArticlesAPIList.as_view()),
    # ����������/��������� ������ ��������������� ������������
    path('api/v1/user/update', UserInfoAPIView.as_view()),
    # ����������/�������� �� ����������
    path('api/v1/articles/favorite/', FavoriteAPIView.as_view()),
    # ����/������� ������/�����������
    path('api/v1/vote/', VoteAPIView.as_view()),
    # ����������/���������/�������� ������������
    path('api/v1/object/comments', CommentsAPIList.as_view()),
    path('api/v1/object/comment', CommentAPIView.as_view()),
    # �����������
    path('api/v1/auth/', include('rest_framework.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken'))
]
