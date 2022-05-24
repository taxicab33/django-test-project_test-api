from django.contrib.auth import logout, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView
from .forms import *
from .models import *
from .utils import DataMixin


class NewsHome(DataMixin, ListView):
    model = Article
    template_name = 'newsapp/main.html'
    context_object_name = 'articles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        sorted_articles = self.get_sorted_articles(articles=context['articles'])
        return dict(list(context.items()) + list(c_def.items()) + list(sorted_articles.items()))

    def get_queryset(self):
        return Article.objects.filter(is_published=True).select_related('user', 'cat', 'user__userprofile')


class ShowCategories(DataMixin, ListView):
    model = Article
    template_name = 'newsapp/main.html'
    context_object_name = 'articles'
    allow_empty = False

    def get_queryset(self, **kwargs):
        return Article.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)\
            .select_related('user', 'cat', 'user__userprofile')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Тема - ' + c.name)
        sorted_articles = self.get_sorted_articles(articles=context['articles'])
        return dict(list(c_def.items()) + list(sorted_articles.items()))


class ShowArticle(DetailView, DataMixin):
    model = Article
    template_name = 'newsapp/article.html'
    slug_url_kwarg = 'article_slug'
    context_object_name = 'article'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['object'].title)
        self.update_views(context['article'])
        return dict(list(context.items()) + list(c_def.items()))

    def get_object(self):
        return self.model.objects.select_related('user', 'cat', 'user__userprofile')\
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
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))




