from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_currentuser.middleware import (
get_current_user, get_current_authenticated_user)
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import request
from django.urls import reverse
from django.contrib.auth.models import User

from comments.models import Comment
from favorites.models import Favorite
from newsapp.model_services import gen_slug, gen_user_slug
from votes.models import LikeDislike


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, blank=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Изображение", null=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создание")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    tags = models.TextField(blank=True, verbose_name="Тэги")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категория")
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, verbose_name='Автор', related_name='author')
    views = models.IntegerField(default=0)  # в следующий раз сделать отдельным классов выше
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)

    votes = GenericRelation(LikeDislike, related_query_name='article_likes')
    comments = GenericRelation(Comment, related_query_name='article_comments')
    is_user_favorite = bool

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article', kwargs={'article_slug': self.slug})

    def get_rating(self):
        return self.likes - self.dislikes

    def in_user_favorites(self):
        if Favorite.objects.get(object_id=self.pk, content_type=ContentType.objects.get_for_model(self),
                                user=get_current_user()) is not None:
            self.is_user_favorite = True
        else:
            self.is_user_favorite = False

    class Meta:
        verbose_name = "Статьи"
        verbose_name_plural = "Статьи"
        ordering = ['-time_create']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, blank=True, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cat', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = "Категории новостей"
        verbose_name_plural = "Категории"
        ordering = ['id']

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.name)
        super().save(*args, **kwargs)
