# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Endpoint',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('url', models.URLField()),
                ('expected_text', models.TextField()),
                ('is_active', models.BooleanField(default=True, db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ping',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('disposition', models.SmallIntegerField(db_index=True, choices=[(0, 'Passed'), (1, 'Timed out'), (2, 'Failed')])),
                ('response_time', models.DurationField()),
                ('response', models.TextField()),
                ('endpoint', models.ForeignKey(related_name='pings', to='pinger.Endpoint')),
            ],
        ),
        migrations.AddField(
            model_name='endpoint',
            name='group',
            field=models.ForeignKey(related_name='endpoints', to='pinger.Group'),
        ),
        migrations.AddField(
            model_name='endpoint',
            name='subscribers',
            field=models.ForeignKey(related_name='endpoints', to=settings.AUTH_USER_MODEL),
        ),
    ]
