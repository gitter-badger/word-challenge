# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0002_draw_work'),
    ]

    operations = [
        migrations.AlterField(
            model_name='draw',
            name='word',
            field=models.ForeignKey(related_name='draws', to='words.Word'),
        ),
    ]
