from newsapp.models import Article  # Используется при запросе оценки поста, не удалять
from comments.models import Comment  # Используется при запросе оценки комментария, не удалять


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