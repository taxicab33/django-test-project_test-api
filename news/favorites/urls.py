from django.urls import path
from .views import *

urlpatterns = [
    path('favorite', favorite),
    path('article/<slug:article_slug>/favorite', favorite),
    path('user/<slug:user_slug>/favorite', favorite),
]