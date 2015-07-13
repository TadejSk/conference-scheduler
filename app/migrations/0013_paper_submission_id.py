# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_paper_is_locked'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='submission_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
