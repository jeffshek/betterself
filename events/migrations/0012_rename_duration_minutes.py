# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-05-28 03:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_add_activity_events'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supplementevent',
            old_name='duration',
            new_name='duration_minutes',
        ),
    ]
