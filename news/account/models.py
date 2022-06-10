from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from newsapp.model_services import gen_user_slug


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images/users', blank=True, null=True, verbose_name='Изображение профиля')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, null=True, blank=True, verbose_name="URL")
    title = models.CharField(max_length=255, blank=True, verbose_name="Заголовок", null=True)
    description = models.TextField(blank=True, verbose_name="Расскажите о себе", null=True)
    rating = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    @receiver(post_save, sender=User)
    def create_user_or_update_profile(sender, instance, created, **kwargs):
        if created:
            instance.userprofile = UserProfile.objects.create(user=instance, slug=gen_user_slug(instance.username))
            instance.userprofile.save()

    def get_absolute_url(self):
        return reverse('user', kwargs={'user_slug': self.slug})


