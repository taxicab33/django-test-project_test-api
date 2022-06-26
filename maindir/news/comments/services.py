import json
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from comments.models import Comment
from newsapp.models import *


def get_object(request):
    model = ContentType.objects.get(model=request.POST['content_type'])
    try:
        obj = model.get_object_for_this_type(slug=request.POST['object_id'])  # Получаем экземпляр по slug
    except:
        obj = model.get_object_for_this_type(pk=int(request.POST['object_id']))  # Получаем экземпляр по id
    return obj


def comment_action(request):
    obj = get_object(request)
    json_dict = {}

    if request.user.is_authenticated:
        if request.POST['action'] == 'comment':
            # если делается запрос для создания ответа на другой комментарий
            if request.POST['comment_id'] != '':
                comment_parent = Comment.objects.get(pk=request.POST['comment_id'])
                comment = obj.comments.create(user_id=request.user.pk,
                                              text=request.POST['comment_text'],
                                              object_id=obj.id,
                                              parent=comment_parent)
            # создание нового комментария
            else:
                comment = obj.comments.create(user_id=request.user.pk,
                                              text=request.POST['comment_text'],
                                              object_id=obj.id)
            if request.user.userprofile.avatar:
                json_dict['author_img'] = request.user.userprofile.avatar.url
            json_dict['author_url'] = request.user.userprofile.get_absolute_url()
            json_dict['author_username'] = request.user.username
            json_dict['article_slug'] = obj.slug
            json_dict['comment'] = serializers.serialize("json", Comment.objects.filter(pk=comment.pk))
        else:
            comment = Comment.objects.get(pk=request.POST['comment_id'])
            if request.POST['action'] == 'edit_comment':
                comment.text = request.POST['comment_text']
                comment.save(update_fields=['text', 'time_update'])
                json_dict['comment'] = serializers.serialize("json", Comment.objects.filter(pk=comment.pk))
            elif request.POST['action'] == 'delete_comment':
                comment.delete()
            json_dict['comment_id'] = request.POST['comment_id']
    else:
        json_dict['auth_error'] = "Для данного действия необходимо авторизоваться"
    json_dict['comments_count'] = obj.comments.count()

    return json_dict
