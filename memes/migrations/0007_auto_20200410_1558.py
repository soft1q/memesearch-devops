# Generated by Django 3.0.5 on 2020-04-10 12:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('memes', '0006_memes_is_mark_up_added'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='memes',
            name='owner',
        ),
        migrations.AddField(
            model_name='memes',
            name='owner',
            field=models.ManyToManyField(null=True, related_name='ownImages', to=settings.AUTH_USER_MODEL),
        ),
    ]
