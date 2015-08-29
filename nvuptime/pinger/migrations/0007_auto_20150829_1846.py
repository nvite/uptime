# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pinger', '0006_auto_20150829_1824'),
    ]

    operations = [
        migrations.RenameField(
            model_name='endpoint',
            old_name='name',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='group',
            old_name='name',
            new_name='title',
        ),
    ]
