from django.contrib.auth import update_session_auth_hash, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

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
        c_def = self.get_user_context(title='Регистрация пользователя')
        return dict(list(context.items()) + list(c_def.items()))

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
        c_def = self.get_user_context(title='Регистрация пользователя')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('main')


class ShowUserProfile(DataMixin, DetailView):
    model = UserProfile
    slug_url_kwarg = 'user_slug'
    template_name = 'account/user_profile.html'
    context_object_name = 'required_user'
    object_list = 'required_user_articles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_articles = self.get_user_articles(required_user=context['required_user'].user)
        c_def = self.get_user_context(title=context['required_user'].user.username)
        return dict(list(context.items()) + list(c_def.items()) + list(user_articles.items()))


@login_required
def update_user_info(request, **kwargs):
    user = request.user
    userprofile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        user_form = UserEditForm(instance=user, data=request.POST)
        profile_form = UserProfileEditForm(instance=userprofile,
                                           data=request.POST, files=request.FILES)
        change_password_form = UserPasswordEditForm(user=user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
        if profile_form.is_valid():
            profile_form.save()
        if change_password_form.is_valid():
            change_password_form.save()
        # Обновляем сессию, чтобы auth_user не вышел из аккаунта
        update_session_auth_hash(request, user)
        return HttpResponseRedirect(userprofile.get_absolute_url())
    else:
        user_form = UserEditForm(instance=user)
        profile_form = UserProfileEditForm(instance=userprofile)
        change_password_form = UserPasswordEditForm(user=user)
        return render(request,
                      'account/update_user_info.html',
                      {'user_form': user_form,
                       'profile_form': profile_form,
                       'change_password_form': change_password_form})


@login_required
def logout_user(request):
    logout(request)
    return redirect('main')


class ShowUserLikedArticles(DataMixin, DetailView):
    model = UserProfile
    slug_url_kwarg = 'user_slug'
    template_name = 'account/liked_articles.html'
    context_object_name = 'required_user'
    object_list = 'articles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = self.get_user_liked_articles(required_user=context['required_user'].user)
        c_def = self.get_user_context(title="Понравившиеся статьи")
        return dict(list(context.items()) + list(c_def.items()))


class ShowUserFavoriteArticles(DataMixin, DetailView):
    model = UserProfile
    slug_url_kwarg = 'user_slug'
    template_name = 'account/liked_articles.html'
    context_object_name = 'required_user'
    object_list = 'articles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = self.get_user_favorite_articles(required_user=context['required_user'].user)
        c_def = self.get_user_context(title="Избранные статьи")
        return dict(list(context.items()) + list(c_def.items()))