# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pinger', '0010_auto_20151005_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outage',
            name='title',
            field=models.CharField(max_length=255, default='Failed Automated System Checks'),
        ),
    ]
