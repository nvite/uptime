# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pinger', '0002_auto_20150829_0357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endpoint',
            name='expected_status',
            field=models.SmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
