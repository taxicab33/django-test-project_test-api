from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render
from account.forms import *
from account.models import UserProfile
from newsapp.model_services import gen_user_slug
from newsapp.models import Category


class UserMixin:

    def save_user_forms(self):
        request = self.request
        user = request.user
        userprofile = UserProfile.objects.get(user=user)
        user_form = UserEditForm(instance=user, data=request.POST)
        profile_form = UserProfileEditForm(instance=userprofile,
                                           data=request.POST, files=request.FILES)
        change_password_form = UserPasswordEditForm(user=user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
            userprofile.slug = gen_user_slug(request.POST['username'])
            userprofile.save()
        if profile_form.is_valid():
            profile_form.save()
        if change_password_form.is_valid():
            change_password_form.save()
        # Обновляем сессию, чтобы auth_user не вышел из аккаунта
        update_session_auth_hash(request, user)
        return {'user': user, 'userprofile': userprofile}

    def get_user_forms(self):
        request = self.request
        context = {}
        user = request.user
        userprofile = UserProfile.objects.get(user=user)
        context['user_form'] = UserEditForm(instance=user)
        context['profile_form'] = UserProfileEditForm(instance=userprofile)
        context['change_password_form'] = UserPasswordEditForm(user=user)
        context['title'] = "Profile Update"
        context['cats'] = Category.objects.all()
        return render(request, 'account/update_user_info.html', context)
