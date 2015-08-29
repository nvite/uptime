# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pinger', '0003_auto_20150829_0408'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ping',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterField(
            model_name='ping',
            name='response_time',
            field=models.DecimalField(max_digits=10, decimal_places=6),
        ),
    ]
