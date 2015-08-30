# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pinger', '0007_auto_20150829_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='endpoint',
            name='ping_interval',
            field=models.DurationField(default=datetime.timedelta(0, 300)),
        ),
        migrations.AddField(
            model_name='group',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
