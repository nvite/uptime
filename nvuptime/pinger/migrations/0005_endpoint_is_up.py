# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pinger', '0004_auto_20150829_0516'),
    ]

    operations = [
        migrations.AddField(
            model_name='endpoint',
            name='is_up',
            field=models.BooleanField(db_index=True, default=True),
        ),
    ]
