from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

from account.models import UserProfile


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'input-group inputs mb-2 mt-2'}))
    email = forms.CharField(label='Электронная почта',
                            widget=forms.TextInput(attrs={'class': 'input-group inputs mb-2 mt-2'}))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'input-group inputs mb-2 mt-2'}))
    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={'class': 'input-group inputs mb-2 mt-2'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'input-group inputs mb-2 mt-2'}),
            'first_name': forms.TextInput(attrs={'class': 'input-group inputs mb-2 mt-2'}),
            'username': forms.TextInput(attrs={'class': 'input-group inputs mb-2 mt-2'}),
            'email': forms.TextInput(attrs={'class': 'input-group inputs mb-2 mt-2'}),
            'password1': forms.PasswordInput(attrs={'class': 'input-group inputs mb-2 mt-2'}),
            'password2': forms.PasswordInput(attrs={'class': 'input-group inputs mb-2 mt-2'}),
        }


class UserEditForm(forms.ModelForm):
    username = forms.CharField(label='Логин', required=True,
                               widget=forms.TextInput(attrs={'class': 'input-group inputs mb-2 mt-2'}))


    class Meta(RegisterUserForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  )


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar', 'title', 'description')
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'input-group inputs mb-2 mt-2'}),
            'title': forms.TextInput(attrs={'class': 'input-group inputs md-left mb-2 mt-2'}),
            'description': forms.Textarea(attrs={'class': 'input-group inputs mb-2 mt-2'}),
        }


class UserPasswordEditForm(PasswordChangeForm):
    old_password = forms.CharField(label='Введите старый пароль:', required=False,
                                   widget=forms.PasswordInput(attrs={'class': 'input-group inputs mb-2 my-2'}))
    new_password1 = forms.CharField(label='Введите новый пароль:', required=False,
                               widget=forms.PasswordInput(attrs={'class': 'input-group inputs mb-2 my-2'}))
    new_password2 = forms.CharField(label='Подтвердите новый пароль:', required=False,
                                           widget=forms.PasswordInput(attrs={'class': 'input-group inputs mb-2 my-2'}))

    class Meta:
        model = User
        fields = ('old_password1', 'new_password1', 'new_password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'input-group inputs mb-2 mt-2'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'input-group inputs mb-2 mt-2'}))
