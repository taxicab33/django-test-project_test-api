# Generated by Django 3.2.9 on 2022-03-08 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0016_delete_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='dislikes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
