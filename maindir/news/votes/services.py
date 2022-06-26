import json

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse

from comments.services import get_object
from newsapp.models import Article  # Используется при запросе оценки поста, не удалять
from comments.models import Comment  # Используется при запросе оценки комментария, не удалять
from votes.models import LikeDislike


def delete_vote(obj, vote_type):
    if vote_type == -1:
        if obj.dislikes > 0:
            obj.dislikes -= 1
    else:
        if obj.likes > 0:
            obj.likes -= 1
    obj.save()


def change_vote(obj, vote_type):
    if vote_type == -1:
        obj.dislikes += 1
        if obj.likes > 0:
            obj.likes -= 1
    else:
        obj.likes += 1
        if obj.dislikes > 0:
            obj.dislikes -= 1
    obj.rating = obj.likes - obj.dislikes
    obj.save()


def add_vote(obj, vote_type):
    if vote_type == -1:
        obj.dislikes += 1
    else:
        obj.likes += 1
    obj.rating = obj.likes - obj.dislikes
    obj.save()


def get_vote_type(request):
    if request.POST['vote_type'] == 'like':  # Тип голоса
        vote_type = 1
    else:
        vote_type = -1
    return vote_type


def vote_logic(self, request, args, kwargs):
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
            obj.votes.create(user=request.user, vote=self.vote_type, object_id=obj.id)
            add_vote(obj, self.vote_type)
            result = True

        return HttpResponse(json.dumps({"result": result, "like_count": obj.likes, "dislike_count": obj.dislikes}),
                            content_type="application/json")
    else:
        return HttpResponse(json.dumps({"auth_error": 'Для данного действия необходимо авторизоваться'}),
                            content_type="application/json")