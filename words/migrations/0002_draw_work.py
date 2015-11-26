# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('words', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Draw',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('accepted', models.NullBooleanField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ('timestamp',),
            },
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('draw', models.OneToOneField(to='words.Draw', serialize=False, primary_key=True, related_name='work')),
                ('language', models.CharField(max_length=5, db_index=True)),
            ],
        ),
        migrations.AddField(
            model_name='draw',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='draw',
            name='word',
            field=models.ForeignKey(to='words.Word'),
        ),
    ]
