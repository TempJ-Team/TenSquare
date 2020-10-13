# Generated by Django 2.2.5 on 2020-10-12 15:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gathering', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='gathering',
            name='users',
            field=models.ManyToManyField(related_name='gathers', to=settings.AUTH_USER_MODEL, verbose_name='参加者'),
        ),
    ]
