# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-01-01 23:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('supplements', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SleepEventLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('source', models.CharField(choices=[('api', 'Api'), ('ios', 'Ios'), ('android', 'Android'), ('web', 'Web'), ('user_excel', 'User_Excel')], max_length=50)),
                ('sleep_time_minutes', models.IntegerField()),
                ('day', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SupplementEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('source', models.CharField(choices=[('api', 'Api'), ('ios', 'Ios'), ('android', 'Android'), ('web', 'Web'), ('user_excel', 'User_Excel')], max_length=50)),
                ('quantity', models.FloatField(default=1)),
                ('time', models.DateTimeField()),
                ('supplement_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplements.Supplement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Supplement Events',
                'ordering': ['user', '-time'],
                'verbose_name': 'Supplement Event',
            },
        ),
    ]
