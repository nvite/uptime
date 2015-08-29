# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pinger', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='endpoint',
            name='expected_status',
            field=models.SmallIntegerField(max_length=3, default=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='endpoint',
            name='timeout',
            field=models.DurationField(default=datetime.timedelta(0, 5)),
        ),
        migrations.AddField(
            model_name='ping',
            name='response_code',
            field=models.SmallIntegerField(db_index=True, default=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ping',
            name='response_headers',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='endpoint',
            name='expected_text',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ping',
            name='disposition',
            field=models.SmallIntegerField(db_index=True, choices=[(0, 'Passed'), (1, 'Timed out'), (2, 'Failed content'), (3, 'Failed')]),
        ),
    ]
