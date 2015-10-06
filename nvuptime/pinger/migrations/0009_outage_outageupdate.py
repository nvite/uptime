# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pinger', '0008_auto_20150830_1849'),
    ]

    operations = [
        migrations.CreateModel(
            name='Outage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('start', models.DateTimeField(auto_now_add=True)),
                ('end', models.DateTimeField()),
            ],
            options={
                'ordering': ('-start',),
            },
        ),
        migrations.CreateModel(
            name='OutageUpdate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.SmallIntegerField(db_index=True, choices=[(0, 'Passed'), (1, 'Timed out'), (2, 'Failed content'), (3, 'Failed')])),
                ('text', models.TextField(default='We are actively investigating a service\n                                       disruption and will post more\n                                       information when available.')),
                ('outage', models.ForeignKey(to='pinger.Outage', related_name='updates')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]
