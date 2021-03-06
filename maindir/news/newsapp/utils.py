from .services import create_pagination_list, create_time_interval_list
from django.contrib.contenttypes.models import ContentType
from account.models import UserProfile
from favorites.models import Favorite
from votes.models import LikeDislike
from .models import Article, Category


class DataMixin:
    paginate_by = 5
    pagination_list = create_pagination_list()
    time_intervals_list = create_time_interval_list()

    @classmethod
    def is_articles_in_user_favorites(self, articles):
        for item in articles:
            item.in_user_favorites()
        return articles

    def get_user_context(self, context):
        context['cats'] = Category.objects.all()
        # запрос при выборке записей
        try:
            if len(context['articles']) > 0:
                context['pagination_list'] = self.pagination_list
                context['picked_sort_list'] = self.request.GET.getlist('sort')
                context['paginate_by'] = str(self.paginate_by)
                context['time_intervals_list'] = self.time_intervals_list
                # проверяем, находятся ли статьи в избранном текущего пользователя
                if self.request.user:
                    context['articles'] = self.is_articles_in_user_favorites(context['articles'])
        except:
            # запрос при получении статьи
            try:
                self.update_views(context['article'])
            # всё остальное
            except:
                pass
        return context

    def get_sorted_articles(self, **kwargs):
        sort_list = []
        # если в GET запросе присутсвуют параметры для сортировки
        if self.request.GET.getlist('sort'):
            sort_list = self.request.GET.getlist('sort')
            # page - переменная для измененения максимального кол-ва записей на странице
            # желательно чтобы, он был последним, или передавать весь сортировочный список в виде словаря и вытаскивать
            # по ключу - page: {'page': '5'}
            if len(sort_list) > 2:
                page = sort_list[-1]
                self.paginate_by = page
                # Весь остальной список сортировки, с названием полей модели
                sort_list = sort_list[0:-1]
        # получаем статьи определённой категории
        if 'cat_slug' in kwargs.keys():
            articles = Article.objects.filter(cat__slug=kwargs['cat_slug'], is_published=True).order_by(*sort_list)\
                .select_related('user', 'cat', 'user__userprofile')
        # получаем все статьи пользователя
        elif 'user' in kwargs.keys():
            url = self.request.path
            user = kwargs['user']
            articles = self.get_user_own_articles(url=url, user=user, sort_list=sort_list)
        # получаем все статьи
        else:
            if len(sort_list) > 0:
                articles = Article.objects.order_by(*sort_list).select_related('user', 'cat', 'user__userprofile')
            else:
                articles = Article.objects.order_by('-time_create').select_related('user', 'cat', 'user__userprofile')
        return articles

    def get_user_own_articles(self, url, user, sort_list):
        user_profile = UserProfile.objects.get(user=user)
        values = {}
        articles = []
        if f'/user/{user_profile.slug}/' in url:
            # если запрашиваем понравившиеся статьи пользователя
            if 'liked_articles' in url:
                values = LikeDislike.objects.filter(user=user, content_type=ContentType.objects.get_for_model(Article))
            # если запрашиваем избранные статьи пользователя
            elif 'favorite_articles' in url:
                values = Favorite.objects.filter(user=user, content_type=ContentType.objects.get_for_model(Article))
                articles = Article.objects.filter(pk__in=values.values('object_id')).order_by(*sort_list).\
                    select_related('user', 'cat', 'user__userprofile')
            else:
                if len(sort_list) > 0:
                    articles = Article.objects.filter(user=user).order_by(*sort_list).\
                        select_related('user', 'cat', 'user__userprofile')
                else:
                    articles = Article.objects.filter(user=user).order_by('-time_create'). \
                        select_related('user', 'cat', 'user__userprofile')

        return articles

    def get_user(self):
        user_slug = str(self.request.path).split('/')[-2]
        user_profile = UserProfile.objects.get(slug=user_slug)
        return user_profile.user

    def update_views(self, article):
        article.views += 1
        article.save()

