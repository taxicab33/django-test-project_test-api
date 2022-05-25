from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

from account.forms import UserEditForm, UserProfileEditForm, UserPasswordEditForm
from account.models import UserProfile


class UserMixin:

    def update_user_info(self, request):
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
