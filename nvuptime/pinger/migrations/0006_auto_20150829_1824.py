# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pinger', '0005_endpoint_is_up'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='endpoint',
            name='subscribers',
        ),
        migrations.AddField(
            model_name='endpoint',
            name='subscribers',
            field=models.ManyToManyField(related_name='endpoints', blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
