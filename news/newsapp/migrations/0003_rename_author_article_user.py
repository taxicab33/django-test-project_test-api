# Generated by Django 3.2.9 on 2022-02-01 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0002_alter_category_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='author',
            new_name='user',
        ),
    ]
