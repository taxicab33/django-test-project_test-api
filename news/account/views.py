from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from account.utils import UserMixin
from account.forms import *
from account.models import UserProfile
from newsapp.models import Article
from newsapp.utils import DataMixin


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Регистрация"
        context = self.get_user_context(context)
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'account/login.html'
    success_url = reverse_lazy('main')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Авторизация"
        context = self.get_user_context(context)
        return context

    def get_success_url(self):
        return reverse_lazy('main')


class ShowUserProfile(DataMixin, ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'account/user_profile.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userprofile'] = UserProfile.objects.get(user=self.get_user())
        context['title'] = context['userprofile'].user.username
        context = self.get_user_context(context)
        return context

    def get_queryset(self):
        user = self.get_user()
        articles = self.get_sorted_articles(user=user)
        return articles


@login_required
def update_user_info(request, **kwargs):
    UserMixin.update_user_info(request)


@login_required
def logout_user(request):
    logout(request)
    return redirect('main')


class ShowUserLikedArticles(DataMixin, ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'account/liked_articles.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userprofile'] = UserProfile.objects.get(user=self.get_user())
        context['title'] = "Понравившиеся статьи"
        context = self.get_user_context(context)
        return context

    def get_queryset(self):
        user = self.get_user()
        articles = self.get_sorted_articles(user=user)
        return articles


class ShowUserFavoriteArticles(DataMixin, ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'account/liked_articles.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userprofile'] = UserProfile.objects.get(user=self.get_user())
        context['title'] = "Избранные статьи"
        context = self.get_user_context(context)
        return context

    def get_queryset(self):
        user = self.get_user()
        articles = self.get_sorted_articles(user=user)
        return articles
