# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-19 11:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CodePointer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=500)),
                ('value', models.BigIntegerField(default=0)),
            ],
        ),
    ]
