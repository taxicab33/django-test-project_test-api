import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.views import View

from comments.services import get_object
from votes.models import LikeDislike
from newsapp.models import Article  # Используется при запросе оценки поста, не удалять
from comments.models import Comment  # Используется при запросе оценки комментария, не удалять
from votes.services import get_vote_type, change_vote, delete_vote, add_vote


class VotesView(View, LoginRequiredMixin):
    model = None  # Модель данных - Статьи или Комментарии
    vote_type = None  # Тип комментария Like/Dislike

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.vote_type = get_vote_type(request)
            obj = get_object(request)
            try:
                likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj),
                                                      object_id=obj.id, user=request.user)
                if likedislike.vote is not self.vote_type:
                    likedislike.vote = self.vote_type
                    likedislike.save(update_fields=['vote'])
                    change_vote(obj, likedislike.vote)
                    result = True
                else:
                    delete_vote(obj, likedislike.vote)
                    likedislike.delete()
                    result = False
            except LikeDislike.DoesNotExist:
                obj.votes.create(user=request.user,
                                 vote=self.vote_type,
                                 object_id=obj.id)
                add_vote(obj, self.vote_type)
                result = True

            return HttpResponse(json.dumps({
                    "result": result,
                    "like_count": obj.likes,
                    "dislike_count": obj.dislikes
                }), content_type="application/json")
        else:
            return HttpResponse(json.dumps
                    ({
                        "auth_error": 'Для данного действия необходимо авторизоваться',
                    }), content_type="application/json")