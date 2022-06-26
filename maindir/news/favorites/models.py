from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Favorite(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создание")
