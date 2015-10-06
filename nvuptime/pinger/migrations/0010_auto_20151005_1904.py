# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pinger', '0009_outage_outageupdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outage',
            name='end',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='outageupdate',
            name='status',
            field=models.SmallIntegerField(db_index=True, choices=[(0, 'Disruption'), (1, 'Watching'), (2, 'Resolved')]),
        ),
        migrations.AlterField(
            model_name='outageupdate',
            name='text',
            field=models.TextField(default='We are actively investigating a service disruption and will post more information when available.'),
        ),
    ]
