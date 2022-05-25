import json
from django.core import serializers
from comments.models import Comment
from newsapp.models import Article


def get_object(request):
    model = globals().get(request.POST['type'])
    try:
        obj = model.objects.get(pk=int(request.POST['obj_id']))  # Получаем экземпляр по id
    except ValueError:
        obj = model.objects.get(slug=request.POST['obj_id'])  # Получаем экземпляр по slug

    return obj


def comment_action(request):
    obj = get_object(request)
    json_dict = {}

    if request.user.is_authenticated:
        if request.POST['action'] == 'comment':
            if request.POST['comment_id'] != '':
                comment_parent = Comment.objects.get(pk=request.POST['comment_id'])
                comment = obj.comments.create(user_id=request.user.pk,
                                              text=request.POST['comment_text'],
                                              object_id=obj.id,
                                              parent=comment_parent)
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
