# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-27 17:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generics', '0002_codepointer_tfield'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='codepointer',
            name='tfield',
        ),
    ]
