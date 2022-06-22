from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .forms import *
from .models import Article, Category
from .services import get_article_related_objects
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
        return self.get_sorted_articles()


class ArticlesCategoryListView(DataMixin, ListView):
    model = Article
    template_name = 'newsapp/main.html'
    context_object_name = 'articles'
    allow_empty = False

    def get_queryset(self):
        return self.get_sorted_articles(cat_slug=self.kwargs['cat_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(slug=self.kwargs['cat_slug'])
        return self.get_user_context(context)


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
        return get_article_related_objects(self.kwargs)


class CreateArticleView(LoginRequiredMixin, DataMixin, CreateView):
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


class UpdateArticleView(UpdateView):
    model = Article
    form_class = CreateArticle
    slug_url_kwarg = 'article_slug'
    template_name = 'newsapp/create_article.html'


class DeleteArticleView(DeleteView):
    success_url = reverse_lazy('main')
    slug_url_kwarg = 'article_slug'
    model = Article

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.success_url)
