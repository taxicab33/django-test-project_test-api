from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from votes.models import LikeDislike


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='Пользователь', on_delete=models.CASCADE)
    text = models.TextField(blank=True, verbose_name="Текст комментария")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    votes = GenericRelation(LikeDislike, related_query_name='comments')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создание")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.CASCADE, blank=True, null=True
    )
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    class Meta:
        ordering = ['-time_create']