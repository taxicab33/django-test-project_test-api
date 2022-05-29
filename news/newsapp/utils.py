from django.contrib.contenttypes.models import ContentType
from django.utils.datetime_safe import datetime

from favorites.models import Favorite
from votes.models import LikeDislike
from .models import Article, Category


class DataMixin:
    max_new_articles = 8
    paginate_by = max_new_articles
    current_datetime = datetime.now()
    week = current_datetime.strftime("%V")

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.all()
        context['cats'] = cats
        return context

    def get_sorted_articles(self, **kwargs):
        kwargs['new_articles'] = Article.objects.filter(time_create=self.current_datetime).order_by(
            '-time_create').select_related('user', 'cat', 'user__userprofile')
        # лучшее за неделю
        kwargs['week_popular_articles'] = Article.objects.filter(time_create__week=self.week).order_by(
            '-views', '-time_create').select_related('user', 'cat', 'user__userprofile')[:self.max_new_articles]
        return kwargs

    def get_user_articles(self, **kwargs):
        kwargs['required_user_articles'] = Article.objects.filter(user=kwargs['required_user'],
                                                                  is_published=True).order_by('-views')\
            .select_related('user', 'cat', 'user__userprofile')
        kwargs['required_user_new_articles'] = Article.objects.filter(user=kwargs['required_user'],
                                                                      time_create=self.current_datetime,
                                                                      is_published=True).order_by('-time_create')\
            .select_related('user', 'cat', 'user__userprofile')
        if len(kwargs['required_user_new_articles']) == 0:
            kwargs['required_user_new_articles'] = (Article.objects.filter(time_create=self.current_datetime,
                                                                           is_published=False).order_by('-time_create'))\
                .select_related('user', 'cat', 'user__userprofile')
        return kwargs

    def get_user_liked_articles(self, **kwargs):
        user_likes = LikeDislike.objects.filter(user=kwargs['required_user'], vote=1,
                                                content_type=ContentType.objects.get_for_model(Article))
        user_liked_articles = Article.objects.filter(pk__in=user_likes.values('object_id'))
        return user_liked_articles

    def get_user_favorite_articles(self, **kwargs):
        user_likes = Favorite.objects.filter(user=kwargs['required_user'],
                                             content_type=ContentType.objects.get_for_model(Article))
        user_liked_articles = Article.objects.filter(pk__in=user_likes.values('object_id'))
        return user_liked_articles

    def update_views(self, article):
        article.views += 1
        article.save()

