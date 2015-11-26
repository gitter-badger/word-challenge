# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='WordTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('language', models.CharField(db_index=True, max_length=5)),
                ('translation', models.CharField(null=True, max_length=100)),
                ('added_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('added_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('word', models.ForeignKey(related_name='translations', to='words.Word')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='wordtranslation',
            unique_together=set([('language', 'translation'), ('word', 'language')]),
        ),
    ]
