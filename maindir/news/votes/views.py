import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from newsapp.models import Article  # Используется при запросе оценки поста, не удалять
from comments.models import Comment  # Используется при запросе оценки комментария, не удалять
from votes.services import vote_logic


class VotesView(View, LoginRequiredMixin):
    model = None  # Модель данных - Статьи или Комментарии
    vote_type = None  # Тип комментария Like/Dislike

    def post(self, request, *args, **kwargs):
        return vote_logic(self, request, args, kwargs)
