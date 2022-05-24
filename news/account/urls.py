from django.urls import path
from django.contrib.auth import views
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('user/<slug:user_slug>/', ShowUserProfile.as_view(), name='user'),
    path('user/<slug:user_slug>/update', update_user_info, name='update_user_info'),
    path('user/<slug:user_slug>/liked_articles', ShowUserLikedArticles.as_view()),
    path('user/<slug:user_slug>/favorite_articles', ShowUserFavoriteArticles.as_view()),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
]


