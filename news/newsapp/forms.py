from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from newsapp.models import Article, Comment


class CreateArticle(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Категория не выбрана"

    class Meta:
        model = Article
        fields = ('title', 'content', 'photo', 'is_published', 'tags', 'cat')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-group inputs mb-2 mt-2'}),
            'content': forms.Textarea(attrs={'class': 'input-group inputs mb-2 mt-2'}),
            'tags': forms.Textarea(attrs={'class': 'input-group inputs mb-2 mt-2'}),
        }
