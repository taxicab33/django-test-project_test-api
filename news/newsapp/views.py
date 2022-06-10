from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView
from .forms import *
from .models import *
from .utils import DataMixin


class ArticlesListView(DataMixin, ListView):
    model = Article
    template_name = 'newsapp/main.html'
    context_object_name = 'articles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Главная страница"
        context = self.get_user_context(context)
        return context

    def get_queryset(self):
        articles = self.get_sorted_articles()
        return articles


class ArticlesCategoryListView(DataMixin, ListView):
    model = Article
    template_name = 'newsapp/main.html'
    context_object_name = 'articles'
    allow_empty = False

    def get_queryset(self):
        articles = self.get_sorted_articles(cat_slug=self.kwargs['cat_slug'])
        return articles

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # получаем выбранную категорию
        context['category'] = Category.objects.get(slug=self.kwargs['cat_slug'])
        context = self.get_user_context(context)
        # получаем категории
        return context


class ArticleDetailView(DetailView, DataMixin):
    model = Article
    template_name = 'newsapp/article.html'
    slug_url_kwarg = 'article_slug'
    context_object_name = 'article'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.get_user_context(context)
        return context

    def get_object(self):
        return Article.objects.select_related('user', 'cat', 'user__userprofile')\
            .prefetch_related('comments', 'comments__parent', 'comments__user__userprofile')\
            .get(slug=self.kwargs['article_slug'])


class CreateArticle(LoginRequiredMixin, DataMixin, CreateView):
    form_class = CreateArticle
    template_name = 'newsapp/create_article.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form_class):
        form_class.instance.user = self.request.user
        return super().form_valid(form_class)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Добавление статьи"
        context = self.get_user_context(context)
        return context




