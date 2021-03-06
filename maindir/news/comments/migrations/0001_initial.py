# Generated by Django 3.2.9 on 2022-05-26 16:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, verbose_name='Текст комментария')),
                ('object_id', models.PositiveIntegerField()),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время создание')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('likes', models.IntegerField(default=0)),
                ('dislikes', models.IntegerField(default=0)),
                ('rating', models.IntegerField(default=0)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comments.comment', verbose_name='Родитель')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Пользователь', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-time_create'],
            },
        ),
    ]
