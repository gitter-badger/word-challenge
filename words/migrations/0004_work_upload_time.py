# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0003_draw_word_related'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='upload_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
